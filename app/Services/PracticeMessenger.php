<?php

namespace App\Services;

use App\Enums\SubmissionMode;
use App\Models\NodeStep;
use App\Models\Practice;
use App\Models\PracticeMessage;
use App\Models\SavedPractice;
use App\Models\User;
use App\Notifications\PlatformNotification;
use Illuminate\Support\Str;

/**
 * Consultas por práctica (D63), por micro-misión (D110) y por práctica guardada (D124): mandar un mensaje, avisar al otro lado y marcar como
 * leído. El mensaje del alumno lleva la foto del código que tenía en el editor y de lo que le dio al ejecutar.
 */
class PracticeMessenger
{
    public function send(User $author, Practice|NodeStep|SavedPractice $subject, User $student, string $body, ?string $code = null, ?string $output = null): PracticeMessage
    {
        $fromStudent = $author->id === $student->id;
        $message = PracticeMessage::create([
            'practice_id' => $subject instanceof Practice ? $subject->id : null,
            'node_step_id' => $subject instanceof NodeStep ? $subject->id : null,
            'saved_practice_id' => $subject instanceof SavedPractice ? $subject->id : null,
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
            $notification = new PlatformNotification('message', 'Consulta de '.$student->fullName(), $excerpt, self::adminUrl($subject, $student), 'chat-bubble-left-right');
            $subject instanceof SavedPractice
                ? PlatformNotification::toStaffOf($notification, $student)
                : PlatformNotification::toStaff($notification, $student, $subject->node->course);
        }

        return $message;
    }

    /** Lo que escribió el otro lado queda leído. */
    public function markRead(User $viewer, Practice|NodeStep|SavedPractice $subject, User $student): void
    {
        PracticeMessage::thread($subject, $student)->unreadFor($viewer)->update(['read_at' => now()]);
    }

    /** El título que se ve en la bandeja y en los avisos. */
    public static function title(Practice|NodeStep|SavedPractice $subject): string
    {
        return match (true) {
            $subject instanceof NodeStep => 'Micro-misión «'.$subject->title.'»',
            $subject instanceof SavedPractice => 'Mi práctica «'.$subject->title.'»',
            default => $subject->title,
        };
    }

    /**
     * Donde el alumno ve el hilo: el modo misión si la práctica lleva código; si no, la práctica en el nodo. Una
     * micro-misión, en el nodo con su chat abierto.
     */
    public static function studentUrl(Practice|NodeStep|SavedPractice $subject): string
    {
        if ($subject instanceof SavedPractice) {
            return $subject->url().'#consulta';
        }
        $node = $subject->node;
        if ($subject instanceof NodeStep) {
            return route('student.node', [$node->course, $node]).'?consulta='.$subject->id.'#micro-'.$subject->id;
        }

        return in_array($subject->submission_mode, [SubmissionMode::Code, SubmissionMode::Both], true)
            ? route('student.mission', [$node->course, $node, $subject]).'?panel=messages'
            : route('student.node', [$node->course, $node]).'#practica-'.$subject->id;
    }

    public static function adminUrl(Practice|NodeStep|SavedPractice $subject, User $student): string
    {
        return route('admin.messages', ['hilo' => PracticeMessage::threadKey($subject, $student)]);
    }
}
