<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Str;

/**
 * C++ con Qt obligatorio (docs/historias/cpp.md): la Senda de los Vitrales (S02) pasa a ser la rama R06 del camino,
 * con un nodo nuevo en R06-N03 («Tu clase detrás de la ventana»), y la Encrucijada de los Engranajes pasa de R05-N07
 * al final de R06. Se renombran los códigos de la rama, los nodos, sus prácticas, sus micro-misiones y la insignia del
 * jefe, así el importador los encuentra con su código nuevo (y les pone la rama, el tipo y la moneda nuevos).
 * Corre una sola vez y solo si el curso todavía tiene la numeración vieja (la Gárgola en S02-N04).
 */
return new class extends Migration
{
    private const NODES = ['S02-N01' => 'R06-N01', 'S02-N02' => 'R06-N02', 'S02-N03' => 'R06-N04', 'S02-N04' => 'R06-N05', 'R05-N07' => 'R06-N06'];

    public function up(): void
    {
        $course = DB::table('courses')->where('slug', 'cpp')->first();
        if (! $course) {
            return;
        }
        $gargoyle = DB::table('nodes')->where('course_id', $course->id)->where('code', 'S02-N04')->first();
        if (! $gargoyle || ! str_contains($gargoyle->title, 'Gárgola')) {
            return;
        }

        DB::transaction(function () use ($course) {
            DB::table('branches')->where('course_id', $course->id)->where('code', 'S02')->update(['code' => 'R06']);

            // Los códigos viejos y los nuevos no se cruzan, así que alcanza con un paso.
            $rows = DB::table('nodes')->where('course_id', $course->id)->whereIn('code', array_keys(self::NODES))->get(['id', 'code']);
            foreach ($rows as $row) {
                $from = $row->code;
                $to = self::NODES[$from];
                DB::table('nodes')->where('id', $row->id)->update(['code' => $to]);
                foreach (['practices', 'node_steps'] as $table) {
                    DB::table($table)->where('node_id', $row->id)->where('code', 'like', $from.'-%')->get(['id', 'code'])
                        ->each(fn ($item) => DB::table($table)->where('id', $item->id)->update(['code' => $to.substr($item->code, strlen($from))]));
                }
            }

            $badge = fn (string $code) => Str::slug('cpp-'.$code, '_');
            DB::table('badges')->where('code', $badge('S02-N04'))->update(['code' => $badge('R06-N05')]);
        });
    }

    public function down(): void
    {
        // No se deshace: el curso de C++ ya tiene la numeración nueva en cursos/cpp/.
    }
};
