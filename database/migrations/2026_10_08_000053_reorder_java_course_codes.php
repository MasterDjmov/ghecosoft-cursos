<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

/**
 * Java según el programa de la cátedra (docs/historias/java.md § 2): las Corrientes pasan a R04, la Torre del
 * Arquitecto (con lo de Spring) a R05, y la Bóveda, el Palacio, el Arcade y JPA pasan a ser Sendas. Se renombran
 * los códigos de las ramas, los nodos, sus prácticas, sus micro-misiones y las insignias de los jefes, así el
 * importador los encuentra con su código nuevo y no crea nodos repetidos: nadie pierde lo que tenía.
 * Corre una sola vez y solo si el curso todavía tiene el orden viejo (la rama S02 es la de las Corrientes).
 */
return new class extends Migration
{
    private const BRANCHES = ['S02' => 'R04', 'R04' => 'S01', 'R05' => 'S02', 'S01' => 'S03', 'S03' => 'S04'];

    public function up(): void
    {
        $course = DB::table('courses')->where('slug', 'java')->first();
        if (! $course) {
            return;
        }
        $old = DB::table('branches')->where('course_id', $course->id)->where('code', 'S02')->first();
        if (! $old || ! str_contains($old->title, 'Corrientes')) {
            return;
        }

        DB::transaction(function () use ($course) {
            $nodes = $this->nodeMap();

            // En dos pasos (primero a un código provisorio), porque los códigos nuevos y los viejos se cruzan.
            $this->rename('branches', $course->id, self::BRANCHES);
            $this->rename('nodes', $course->id, $nodes);

            foreach ($nodes as $from => $to) {
                $node = DB::table('nodes')->where('course_id', $course->id)->where('code', $to)->first();
                if (! $node) {
                    continue;
                }
                foreach (['practices', 'node_steps'] as $table) {
                    DB::table($table)->where('node_id', $node->id)->where('code', 'like', $from.'-%')->get(['id', 'code'])
                        ->each(fn ($row) => DB::table($table)->where('id', $row->id)->update(['code' => $to.substr($row->code, strlen($from))]));
                }
            }

            $badge = fn (string $code) => Str::slug('java-'.$code, '_');
            $badges = DB::table('badges')->whereIn('code', array_map($badge, array_keys($nodes)))->get(['id', 'code']);
            foreach ($badges as $row) {
                DB::table('badges')->where('id', $row->id)->update(['code' => 'tmp_reorder_'.$row->id]);
            }
            foreach ($nodes as $from => $to) {
                $row = $badges->firstWhere('code', $badge($from));
                $row && DB::table('badges')->where('id', $row->id)->update(['code' => $badge($to)]);
            }
        });
    }

    /** @return array<string, string> */
    private function nodeMap(): array
    {
        $map = [];
        foreach (range(1, 8) as $k) {
            $map["R04-N0{$k}"] = "S01-N0{$k}";
            $map["R05-N0{$k}"] = "S02-N0{$k}";
        }
        foreach (range(1, 4) as $k) {
            $map["S01-N0{$k}"] = "S03-N0{$k}";
        }

        return $map + [
            'S02-N01' => 'R04-N01', 'S02-N02' => 'R04-N02', 'S02-N03' => 'R04-N03', 'S02-N04' => 'R04-N05', 'S02-N05' => 'R04-N06',
            'S03-N01' => 'R05-N03', 'S03-N02' => 'R05-N04', 'S03-N03' => 'R05-N05', 'R05-N09' => 'R05-N07',
            'S03-N04' => 'S04-N01', 'S03-N05' => 'S04-N02',
        ];
    }

    /** @param  array<string, string>  $map */
    private function rename(string $table, int $courseId, array $map): void
    {
        $rows = DB::table($table)->where('course_id', $courseId)->whereIn('code', array_keys($map))->get(['id', 'code']);
        foreach ($rows as $row) {
            DB::table($table)->where('id', $row->id)->update(['code' => 'tmp-'.$row->id]);
        }
        foreach ($rows as $row) {
            DB::table($table)->where('id', $row->id)->update(['code' => $map[$row->code]]);
        }
    }

    public function down(): void
    {
        // No se deshace: el curso de Java ya tiene el orden nuevo en cursos/java/.
    }
};
