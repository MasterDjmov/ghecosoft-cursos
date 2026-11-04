<?php

namespace App\Services;

use App\Models\Course;
use App\Models\CourseCompletion;
use App\Models\Expedition;
use App\Models\Hero;
use App\Models\Submission;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Storage;

/**
 * Reiniciar el propio progreso en un curso (D117), para volver a probarlo de cero sin crear otra cuenta. Lo pide cada
 * uno para sí mismo, desde el árbol, y no toca los otros cursos ni el abono: queda como recién inscripto, con las
 * monedas para abrir el raíz. Las monedas y la XP las borra el Ledger.
 *
 * El oro y los ítems son de toda la cuenta y se pueden haber gastado o usado en otro curso: se quedan, y sus movimientos
 * también, así las micro-misiones no los vuelven a pagar. Si no, reiniciar serviría para juntar oro sin fin.
 */
class CourseRestarter
{
    /** Lo que borra del curso. Un test revisa que estén todas. */
    public const WIPED = [
        'expeditions', 'heroes', 'coin_transactions', 'xp_transactions', 'node_step_completions', 'step_attempts', 'node_visits',
        'practice_grants', 'node_unlocks', 'practice_marks', 'submission_comments', 'submissions', 'course_completions', 'user_badges',
    ];

    /**
     * Lo que se conserva: lo de toda la cuenta (ítems, monturas, talleres, ranking histórico, votos), lo pagado (abonos y
     * solicitudes) y las consultas y recordatorios del docente, que no son progreso.
     */
    public const KEPT = [
        'crafts', 'mounts', 'item_movements', 'ranking_snapshots', 'universe_votes',
        'course_subscriptions', 'enrollment_requests', 'practice_messages', 'delay_reminders',
    ];

    public function __construct(private readonly Ledger $ledger, private readonly Heroes $heroes) {}

    public function restart(User $user, Course $course): void
    {
        DB::transaction(function () use ($user, $course) {
            $nodeIds = $course->nodes()->pluck('id');
            $practiceIds = DB::table('practices')->whereIn('node_id', $nodeIds)->pluck('id');
            $stepIds = DB::table('node_steps')->whereIn('node_id', $nodeIds)->pluck('id');
            $submissions = Submission::where('user_id', $user->id)->whereIn('practice_id', $practiceIds);
            $files = (clone $submissions)->pluck('file_path')->filter()->unique()->values()->all();

            // Primero las expediciones: apuntan al héroe. El héroe devuelve el oro que gastó en atributos.
            Expedition::where('user_id', $user->id)->where('course_id', $course->id)->delete();
            Hero::where('user_id', $user->id)->where('course_id', $course->id)->get()
                ->each(fn (Hero $hero) => $this->heroes->reset($hero, $user));

            $this->ledger->forgetCourse($user, $course);

            DB::table('submission_comments')->whereIn('submission_id', (clone $submissions)->select('id'))->delete();
            $submissions->delete();

            $own = fn (string $table) => DB::table($table)->where('user_id', $user->id);
            $own('node_step_completions')->whereIn('node_step_id', $stepIds)->delete();
            $own('step_attempts')->where('course_id', $course->id)->delete();
            $own('node_visits')->where('course_id', $course->id)->delete();
            $own('practice_grants')->whereIn('node_id', $nodeIds)->delete();
            $own('node_unlocks')->whereIn('node_id', $nodeIds)->delete();
            $own('practice_marks')->whereIn('practice_id', $practiceIds)->delete();
            CourseCompletion::where('user_id', $user->id)->where('course_id', $course->id)->delete();

            // Las insignias del curso y las de sus nodos (los jefes).
            $own('user_badges')->whereIn('badge_id', DB::table('badges')->where('course_id', $course->id)->select('id')
                ->union(DB::table('nodes')->whereIn('id', $nodeIds)->whereNotNull('badge_id')->select('badge_id')))->delete();

            DB::afterCommit(function () use ($files) {
                Storage::disk('local')->delete($files);
                Ranking::forget();
            });
        });
    }
}
