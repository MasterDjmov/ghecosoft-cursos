<?php

namespace App\Livewire\Student;

use App\Enums\RequestStatus;
use App\Models\Course;
use App\Models\Node;
use App\Models\NodeUnlock;
use App\Services\TreeAccess;
use Livewire\Attributes\Title;
use Livewire\Component;

/** Mapa de mundos: cada curso publicado es una isla con su estado para el alumno. */
#[Title('Mundos')]
class Worlds extends Component
{
    public function render(TreeAccess $access)
    {
        $user = auth()->user();

        $worlds = Course::where('is_published', true)
            ->orderBy('position')
            ->get()
            ->map(function (Course $course) use ($user, $access) {
                $total = Node::where('course_id', $course->id)->where('is_published', true)->count();
                $unlockedIds = NodeUnlock::where('user_id', $user->id)
                    ->whereHas('node', fn ($q) => $q->where('course_id', $course->id))
                    ->pluck('node_id');
                $completed = Node::whereIn('id', $unlockedIds)->get()
                    ->filter(fn (Node $node) => $access->requiredPracticesApproved($user, $node))
                    ->count();

                $subscription = $access->activeSubscription($user, $course);
                $rootOpen = $unlockedIds->isNotEmpty() && $access->isRootOpen($user, $course);
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

                return compact('course', 'total', 'completed', 'subscription', 'status');
            });

        return view('livewire.student.worlds', ['worlds' => $worlds]);
    }
}
