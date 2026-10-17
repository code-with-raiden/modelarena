import { useState } from 'react'
import EvalPage from './pages/EvalPage'
import HistoryPage from './pages/HistoryPage'
import styles from './App.module.css'

const NAV = [
  { id: 'eval',    label: '⬡ Evaluate',  icon: '🧪' },
  { id: 'history', label: 'History',      icon: '📋' },
]

export default function App() {
  const [page, setPage] = useState('eval')

  return (
    <div className={styles.layout}>
      <aside className={styles.sidebar}>
        <div className={styles.logo}>
          <span className={styles.logoIcon}>⬡</span>
          <span>Model<strong>Arena</strong></span>
        </div>
        <nav className={styles.nav}>
          {NAV.map(n => (
            <button
              key={n.id}
              className={`${styles.navBtn} ${page === n.id ? styles.active : ''}`}
              onClick={() => setPage(n.id)}
            >
              <span>{n.icon}</span> {n.label}
            </button>
          ))}
        </nav>
        <div className={styles.sidebarBottom}>
          <a href="http://localhost:8000/docs" target="_blank" rel="noreferrer"
            className={styles.docsLink}>📖 API Docs</a>
          <a href="https://github.com/code-with-raiden/modelarena" target="_blank" rel="noreferrer"
            className={styles.docsLink}>⭐ GitHub</a>
        </div>
      </aside>
      <main className={styles.main}>
        {page === 'eval'    && <EvalPage />}
        {page === 'history' && <HistoryPage />}
      </main>
    </div>
  )
}
