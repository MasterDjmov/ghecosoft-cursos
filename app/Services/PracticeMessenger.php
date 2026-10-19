<?php

namespace App\Services;

use App\Enums\SubmissionMode;
use App\Models\NodeStep;
use App\Models\Practice;
use App\Models\PracticeMessage;
use App\Models\User;
use App\Notifications\PlatformNotification;
use Illuminate\Support\Str;

/**
 * Consultas por práctica (D63) y por micro-misión (D110): mandar un mensaje, avisar al otro lado y marcar como
 * leído. El mensaje del alumno lleva la foto del código que tenía en el editor y de lo que le dio al ejecutar.
 */
class PracticeMessenger
{
    public function send(User $author, Practice|NodeStep $subject, User $student, string $body, ?string $code = null, ?string $output = null): PracticeMessage
    {
        $fromStudent = $author->id === $student->id;
        $message = PracticeMessage::create([
            'practice_id' => $subject instanceof Practice ? $subject->id : null,
            'node_step_id' => $subject instanceof NodeStep ? $subject->id : null,
            'student_id' => $student->id,
            'author_id' => $author->id,
            'body' => trim($body),
            'code' => $fromStudent && filled($code) ? Str::limit($code, 20000, '') : null,
            'output' => $fromStudent && filled($output) ? Str::limit($output, 5000, '') : null,
        ]);

        $excerpt = self::title($subject).': '.Str::limit(trim($body), 120);
        if ($author->isStaff()) {
            $student->notify(new PlatformNotification('message', 'El profe te respondió', $excerpt, self::studentUrl($subject), 'chat-bubble-left-right'));
        } else {
            PlatformNotification::toStaff(new PlatformNotification('message', 'Consulta de '.$student->fullName(), $excerpt, self::adminUrl($subject, $student), 'chat-bubble-left-right'), $student, $subject->node->course);
        }

        return $message;
    }

    /** Lo que escribió el otro lado queda leído. */
    public function markRead(User $viewer, Practice|NodeStep $subject, User $student): void
    {
        PracticeMessage::thread($subject, $student)->unreadFor($viewer)->update(['read_at' => now()]);
    }

    /** El título que se ve en la bandeja y en los avisos. */
    public static function title(Practice|NodeStep $subject): string
    {
        return $subject instanceof NodeStep ? 'Micro-misión «'.$subject->title.'»' : $subject->title;
    }

    /**
     * Donde el alumno ve el hilo: el modo misión si la práctica lleva código; si no, la práctica en el nodo. Una
     * micro-misión, en el nodo con su chat abierto.
     */
    public static function studentUrl(Practice|NodeStep $subject): string
    {
        $node = $subject->node;
        if ($subject instanceof NodeStep) {
            return route('student.node', [$node->course, $node]).'?consulta='.$subject->id.'#micro-'.$subject->id;
        }

        return in_array($subject->submission_mode, [SubmissionMode::Code, SubmissionMode::Both], true)
            ? route('student.mission', [$node->course, $node, $subject]).'?panel=messages'
            : route('student.node', [$node->course, $node]).'#practica-'.$subject->id;
    }

    public static function adminUrl(Practice|NodeStep $subject, User $student): string
    {
        return route('admin.messages', ['hilo' => PracticeMessage::threadKey($subject, $student)]);
    }
}
