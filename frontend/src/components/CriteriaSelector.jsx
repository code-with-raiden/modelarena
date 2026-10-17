import s from './CriteriaSelector.module.css'

const ALL_CRITERIA = ['Accuracy', 'Clarity', 'Depth', 'Conciseness', 'Creativity', 'Reasoning']

export default function CriteriaSelector({ criteria, onChange }) {
  const toggle = (c) => {
    const next = new Set(criteria)
    next.has(c) ? next.delete(c) : next.add(c)
    onChange(next)
  }
  return (
    <div className={s.wrap}>
      {ALL_CRITERIA.map(c => (
        <button
          key={c}
          className={`${s.chip} ${criteria.has(c) ? s.on : ''}`}
          onClick={() => toggle(c)}
        >
          {criteria.has(c) ? '✓ ' : ''}{c}
        </button>
      ))}
    </div>
  )
}
