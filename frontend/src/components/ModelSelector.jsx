import s from './ModelSelector.module.css'

const ICONS = {
  'OpenRouter': '🔀', 'Anthropic': '🔷',
  'OpenAI': '⚡', 'Groq': '🦙',
  'Google': '💎', 'Mistral': '🌊',
}

export default function ModelSelector({ models, loading, selected, onChange }) {
  const toggle = (id) => {
    const next = new Set(selected)
    next.has(id) ? next.delete(id) : next.add(id)
    onChange(next)
  }

  const selectAll = () => onChange(new Set(models.map(m => m.id)))
  const clearAll  = () => onChange(new Set())

  // Group by recommended vs direct
  const recommended = models.filter(m => m.recommended || m.key_required === 'openrouter')
  const direct      = models.filter(m => !m.recommended && m.key_required !== 'openrouter')

  if (loading) return <div className={s.loading}>Loading models…</div>

  return (
    <div className={s.wrap}>
      <div className={s.toolbar}>
        <button className={s.toolBtn} onClick={selectAll}>All</button>
        <button className={s.toolBtn} onClick={clearAll}>None</button>
        <button className={s.toolBtn} onClick={() => onChange(new Set(recommended.slice(0,5).map(m=>m.id)))}>
          Top 5
        </button>
      </div>
      <div className={s.list}>
        {recommended.length > 0 && (
          <>
            <div className={s.groupLabel}>Via OpenRouter</div>
            {recommended.map(m => (
              <ModelRow key={m.id} model={m} checked={selected.has(m.id)} onToggle={toggle} icons={ICONS} />
            ))}
          </>
        )}
        {direct.length > 0 && (
          <>
            <div className={s.groupLabel}>Direct Keys</div>
            {direct.map(m => (
              <ModelRow key={m.id} model={m} checked={selected.has(m.id)} onToggle={toggle} icons={ICONS} />
            ))}
          </>
        )}
      </div>
    </div>
  )
}

function ModelRow({ model, checked, onToggle, icons }) {
  const shortId = model.id.split('/').pop()
  const icon = icons[model.provider] || '🤖'
  return (
    <label className={`${s.row} ${checked ? s.checked : ''}`}>
      <input type="checkbox" checked={checked} onChange={() => onToggle(model.id)} className={s.checkbox} />
      <span className={s.icon}>{icon}</span>
      <span className={s.name}>{shortId}</span>
      <span className={s.provider}>{model.provider}</span>
    </label>
  )
}
