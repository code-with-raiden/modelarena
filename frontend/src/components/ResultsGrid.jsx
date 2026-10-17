import { RadarChart, PolarGrid, PolarAngleAxis, Radar, ResponsiveContainer, Tooltip } from 'recharts'
import s from './ResultsGrid.module.css'

function scoreColor(v) {
  if (v >= 8) return 'var(--green)'
  if (v >= 6) return 'var(--yellow)'
  return 'var(--red)'
}

function Medal({ rank }) {
  if (rank === 0) return <span className={`${s.medal} ${s.gold}`}>🥇 #1</span>
  if (rank === 1) return <span className={`${s.medal} ${s.silver}`}>🥈 #2</span>
  if (rank === 2) return <span className={`${s.medal} ${s.bronze}`}>🥉 #3</span>
  return <span className={`${s.medal} ${s.other}`}>#{rank + 1}</span>
}

function RadarCard({ evaluation }) {
  const data = Object.entries(evaluation.scores || {}).map(([key, val]) => ({
    subject: key.slice(0, 5),
    value: val,
  }))
  return (
    <ResponsiveContainer width="100%" height={140}>
      <RadarChart data={data}>
        <PolarGrid stroke="var(--border)" />
        <PolarAngleAxis dataKey="subject" tick={{ fill: 'var(--muted)', fontSize: 10 }} />
        <Radar dataKey="value" stroke="var(--accent)" fill="var(--accent)" fillOpacity={0.15} />
        <Tooltip
          contentStyle={{ background: 'var(--surface)', border: '1px solid var(--border)', borderRadius: 6 }}
          labelStyle={{ color: 'var(--muted)' }}
          itemStyle={{ color: 'var(--accent)' }}
        />
      </RadarChart>
    </ResponsiveContainer>
  )
}

export default function ResultsGrid({ result }) {
  const sorted = [...(result.evaluations || [])].sort((a, b) => b.overall - a.overall)
  const winner = result.winner

  return (
    <div>
      {/* Summary bar */}
      <div className={s.summary}>
        <div className={s.stat}>
          <div className={s.statVal} style={{ color: 'var(--accent)' }}>
            {winner?.split('/').pop() || '—'}
          </div>
          <div className={s.statLabel}>Winner</div>
        </div>
        <div className={s.stat}>
          <div className={s.statVal}>
            {sorted.length > 0
              ? (sorted.reduce((a, b) => a + b.overall, 0) / sorted.length).toFixed(1)
              : '—'}
          </div>
          <div className={s.statLabel}>Avg Score</div>
        </div>
        <div className={s.stat}>
          <div className={s.statVal}>{result.models_tested}</div>
          <div className={s.statLabel}>Models Tested</div>
        </div>
        <div className={s.stat}>
          <div className={s.statVal}>
            {Object.values(result.latencies_ms || {}).length > 0
              ? Math.min(...Object.values(result.latencies_ms)) + 'ms'
              : '—'}
          </div>
          <div className={s.statLabel}>Fastest</div>
        </div>
      </div>

      {/* Insight */}
      {result.comparison && (
        <div className={s.insight}>💡 {result.comparison}</div>
      )}

      {/* Cards */}
      <div className={s.grid}>
        {sorted.map((ev, i) => (
          <div key={ev.model_id} className={`${s.card} ${i === 0 ? s.winner : ''}`}>
            <div className={s.cardHeader}>
              <div className={s.modelName}>{ev.model_id?.split('/').pop()}</div>
              <Medal rank={i} />
            </div>
            <div className={s.overall}>
              <span style={{ color: scoreColor(ev.overall), fontSize: 28, fontWeight: 700 }}>
                {typeof ev.overall === 'number' ? ev.overall.toFixed(1) : ev.overall}
              </span>
              <span className={s.outOf}>/10</span>
            </div>

            {/* Score bars */}
            <div className={s.bars}>
              {Object.entries(ev.scores || {}).map(([k, v]) => (
                <div key={k} className={s.bar}>
                  <div className={s.barLabel}>
                    <span>{k}</span>
                    <span style={{ color: scoreColor(v) }}>{v}</span>
                  </div>
                  <div className={s.barBg}>
                    <div className={s.barFill} style={{
                      width: `${v * 10}%`,
                      background: scoreColor(v),
                    }} />
                  </div>
                </div>
              ))}
            </div>

            {/* Radar */}
            <RadarCard evaluation={ev} />

            {/* Verdict */}
            {ev.strength && <p className={s.strength}>✓ {ev.strength}</p>}
            {ev.weakness && <p className={s.weakness}>⚠ {ev.weakness}</p>}

            {/* Latency */}
            <div className={s.latency}>
              ⏱ {result.latencies_ms?.[ev.model_id] ?? '—'}ms
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}
