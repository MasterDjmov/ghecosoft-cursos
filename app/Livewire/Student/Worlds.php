<?php

namespace App\Livewire\Student;

use App\Enums\RequestStatus;
use App\Models\Course;
use App\Models\CourseInterest;
use App\Models\Hero;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Services\CourseCatalog;
use App\Services\Heroes;
use App\Services\TreeAccess;
use DomainException;
use Flux\Flux;
use Livewire\Attributes\Title;
use Livewire\Component;

/**
 * Mapa de mundos: arriba "Mis cursos" (los que abrió, tiene abono o pidió),
 * abajo "Descubrí más mundos" (publicados en los que no está y "Próximamente").
 */
#[Title('Mundos')]
class Worlds extends Component
{
    public function toggleInterest(int $courseId, CourseCatalog $catalog): void
    {
        try {
            $added = $catalog->toggleInterest(auth()->user(), Course::findOrFail($courseId));
        } catch (DomainException $e) {
            Flux::toast(variant: 'danger', text: $e->getMessage());

            return;
        }

        Flux::toast(variant: 'success', text: $added ? 'Listo: te avisamos cuando salga.' : 'Ya no te avisamos.');
    }

    public function render(TreeAccess $access)
    {
        $user = auth()->user();

        $worlds = Course::inCatalog()
            ->with('paths')
            ->withCount(['nodes as published_nodes_count' => fn ($q) => $q->where('is_published', true)])
            ->orderBy('position')
            ->get()
            ->map(function (Course $course) use ($user, $access) {
                if ($course->isUpcoming()) {
                    return ['course' => $course, 'status' => 'upcoming', 'total' => $course->published_nodes_count];
                }

                $total = $course->published_nodes_count;
                $unlocks = NodeUnlock::where('user_id', $user->id)
                    ->whereHas('node', fn ($q) => $q->where('course_id', $course->id))
                    ->latest('unlocked_at')->latest('id')
                    ->get(['node_id']);
                $nodes = Node::whereIn('id', $unlocks->pluck('node_id'))->get()->keyBy('id');
                $done = $nodes->filter(fn (Node $node) => $access->nodeWorkDone($user, $node));

                $subscription = $access->activeSubscription($user, $course);
                $paidUntil = $subscription ? $access->paidUntil($user, $course) : null;
                $rootOpen = $unlocks->isNotEmpty() && $access->isRootOpen($user, $course);
                $pending = $user->enrollmentRequests()
                    ->where('course_id', $course->id)
                    ->where('status', RequestStatus::Pending)
                    ->exists();

                $status = match (true) {
                    $rootOpen && $subscription !== null => 'active',
                    $rootOpen => 'expired',
                    $subscription !== null => 'ready',
                    $pending => 'pending',
                    default => 'closed',
                };

                // "Seguí donde dejaste": el último nodo que abrió y todavía no completó.
                $current = $unlocks->map(fn ($u) => $nodes->get($u->node_id))
                    ->first(fn (?Node $node) => $node && ! $done->has($node->id));

                // Clase 0 de prueba (D71): sin abono ni raíz abierto, se entra gratis.
                $trialRoot = in_array($status, ['closed', 'pending'], true) && $access->canTryCourse($user, $course) ? $course->rootNode : null;

                return ['course' => $course, 'total' => $total, 'completed' => $done->count(), 'subscription' => $subscription, 'paidUntil' => $paidUntil, 'status' => $status, 'current' => $current, 'trialRoot' => $trialRoot];
            });

        [$mine, $discover] = $worlds->partition(fn ($w) => ! in_array($w['status'], ['closed', 'upcoming']));
        $mine = $mine->values();

        // En el carrusel, cada mundo con su protagonista, con el aspecto que eligió el alumno en ese curso.
        $looks = Hero::where('user_id', $user->id)->pluck('look', 'course_id');
        $mine = $mine->map(function (array $world) use ($looks) {
            $protagonist = Heroes::protagonistOf($world['course']);
            $world['protagonist'] = $protagonist && is_file(public_path('img/protagonistas/'.$protagonist['slug'].'/1.webp'))
                ? ['name' => $protagonist['name'], 'title' => $protagonist['title'], 'image' => Heroes::lookUrl($protagonist, $looks[$world['course']->id] ?? 1)]
                : null;

            return $world;
        });

        return view('livewire.student.worlds', [
            'mine' => $mine,
            // El carrusel arranca en el primer mundo en curso.
            'startAt' => max(0, (int) $mine->search(fn ($w) => $w['status'] === 'active')),
            'discover' => $discover->sortBy(fn ($w) => $w['status'] === 'upcoming' ? 1 : 0)->values(),
            'interested' => CourseInterest::where('user_id', $user->id)->pluck('course_id')->flip(),
            'expiring' => $mine->filter(fn ($w) => $w['status'] === 'active' && $w['paidUntil']->lte(now()->addDays(config('game.subscription_warning_days')))),
        ]);
    }
}
