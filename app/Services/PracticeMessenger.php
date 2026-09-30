<?php

namespace App\Services;

use App\Enums\SubmissionMode;
use App\Models\Practice;
use App\Models\PracticeMessage;
use App\Models\User;
use App\Notifications\PlatformNotification;
use Illuminate\Support\Str;

/** Consultas por práctica (D63): mandar un mensaje, avisar al otro lado y marcar como leído. */
class PracticeMessenger
{
    public function send(User $author, Practice $practice, User $student, string $body): PracticeMessage
    {
        $message = PracticeMessage::create([
            'practice_id' => $practice->id,
            'student_id' => $student->id,
            'author_id' => $author->id,
            'body' => trim($body),
        ]);

        $excerpt = $practice->title.': '.Str::limit(trim($body), 120);
        if ($author->isAdmin()) {
            $student->notify(new PlatformNotification('message', 'El profe te respondió', $excerpt, self::studentUrl($practice), 'chat-bubble-left-right'));
        } else {
            PlatformNotification::toAdmins(new PlatformNotification('message', 'Consulta de '.$student->fullName(), $excerpt, self::adminUrl($practice, $student), 'chat-bubble-left-right'));
        }

        return $message;
    }

    /** Lo que escribió el otro lado queda leído. */
    public function markRead(User $viewer, Practice $practice, User $student): void
    {
        PracticeMessage::thread($practice, $student)->unreadFor($viewer)->update(['read_at' => now()]);
    }

    /** Donde el alumno ve el hilo: el modo misión si la práctica lleva código; si no, la práctica en el nodo. */
    public static function studentUrl(Practice $practice): string
    {
        $node = $practice->node;

        return in_array($practice->submission_mode, [SubmissionMode::Code, SubmissionMode::Both], true)
            ? route('student.mission', [$node->course, $node, $practice]).'?panel=messages'
            : route('student.node', [$node->course, $node]).'#practica-'.$practice->id;
    }

    public static function adminUrl(Practice $practice, User $student): string
    {
        return route('admin.messages', ['hilo' => $practice->id.'-'.$student->id]);
    }
}
