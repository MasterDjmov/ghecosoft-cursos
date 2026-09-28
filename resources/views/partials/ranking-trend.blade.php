{{-- Tendencia ▲▼ respecto de la foto del día anterior (Ranking::trends). --}}
@if ($row['new'])
    <span class="font-mono text-[11px] text-secondary-bright" title="Nuevo en el ranking">nuevo</span>
@elseif ($row['trend'] > 0)
    <span class="font-mono text-[11px] text-success" title="Subió {{ $row['trend'] }} desde ayer">▲{{ $row['trend'] }}</span>
@elseif ($row['trend'] < 0)
    <span class="font-mono text-[11px] text-danger" title="Bajó {{ -$row['trend'] }} desde ayer">▼{{ -$row['trend'] }}</span>
@elseif ($row['trend'] === 0)
    <span class="font-mono text-[11px] text-ink-muted" title="Igual que ayer">—</span>
@endif
