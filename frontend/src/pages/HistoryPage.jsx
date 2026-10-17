import s from './HistoryPage.module.css'

export default function HistoryPage() {
  return (
    <div className={s.page}>
      <h1 className={s.title}>Eval History</h1>
      <p className={s.sub}>Past evaluations will appear here once the database is connected (Phase 2).</p>
      <div className={s.placeholder}>
        <div className={s.icon}>📋</div>
        <div className={s.msg}>No history yet — run your first evaluation!</div>
      </div>
    </div>
  )
}
