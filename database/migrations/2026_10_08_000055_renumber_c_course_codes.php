<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

/**
 * C según el apunte de Programación I (docs/historias/c.md § 5): entran dos nodos nuevos, «El preprocesador y las
 * macros» (R01-N08) y «Pilas y colas» (R03-N04), y los que siguen corren un lugar (el Gólem pasa a R01-N10 y la
 * Sanguijuela a R03-N06). Se renombran los códigos de los nodos, sus prácticas, sus micro-misiones y las insignias de
 * los jefes, así el importador los encuentra con su código nuevo y crea limpios los dos nodos nuevos.
 * Corre una sola vez y solo si el curso todavía tiene la numeración vieja (el Gólem en R01-N09).
 */
return new class extends Migration
{
    private const NODES = ['R01-N08' => 'R01-N09', 'R01-N09' => 'R01-N10', 'R03-N04' => 'R03-N05', 'R03-N05' => 'R03-N06'];

    public function up(): void
    {
        $course = DB::table('courses')->where('slug', 'c')->first();
        if (! $course) {
            return;
        }
        $golem = DB::table('nodes')->where('course_id', $course->id)->where('code', 'R01-N09')->first();
        if (! $golem || ! str_contains($golem->title, 'Gólem')) {
            return;
        }

        DB::transaction(function () use ($course) {
            // En dos pasos (primero a un código provisorio), porque los códigos nuevos y los viejos se cruzan.
            $rows = DB::table('nodes')->where('course_id', $course->id)->whereIn('code', array_keys(self::NODES))->get(['id', 'code']);
            foreach ($rows as $row) {
                DB::table('nodes')->where('id', $row->id)->update(['code' => 'tmp-'.$row->id]);
            }
            foreach ($rows as $row) {
                DB::table('nodes')->where('id', $row->id)->update(['code' => self::NODES[$row->code]]);
            }

            foreach ($rows as $row) {
                $from = $row->code;
                $to = self::NODES[$from];
                foreach (['practices', 'node_steps'] as $table) {
                    DB::table($table)->where('node_id', $row->id)->where('code', 'like', $from.'-%')->get(['id', 'code'])
                        ->each(fn ($item) => DB::table($table)->where('id', $item->id)->update(['code' => $to.substr($item->code, strlen($from))]));
                }
            }

            $badge = fn (string $code) => Str::slug('c-'.$code, '_');
            $badges = DB::table('badges')->whereIn('code', array_map($badge, array_keys(self::NODES)))->get(['id', 'code']);
            foreach ($badges as $row) {
                DB::table('badges')->where('id', $row->id)->update(['code' => 'tmp_renumber_'.$row->id]);
            }
            foreach (self::NODES as $from => $to) {
                $row = $badges->firstWhere('code', $badge($from));
                $row && DB::table('badges')->where('id', $row->id)->update(['code' => $badge($to)]);
            }
        });
    }

    public function down(): void
    {
        // No se deshace: el curso de C ya tiene la numeración nueva en cursos/c/.
    }
};
