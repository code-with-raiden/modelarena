import { useState } from 'react'
import { useMutation, useQuery } from '@tanstack/react-query'
import { fetchModels, runEvaluation } from '../api/client'
import ModelSelector from '../components/ModelSelector'
import CriteriaSelector from '../components/CriteriaSelector'
import ResultsGrid from '../components/ResultsGrid'
import s from './EvalPage.module.css'

const DEFAULT_CRITERIA = ['Accuracy', 'Clarity', 'Depth', 'Conciseness']

export default function EvalPage() {
  const [prompt, setPrompt]       = useState('')
  const [selected, setSelected]   = useState(new Set())
  const [criteria, setCriteria]   = useState(new Set(DEFAULT_CRITERIA))
  const [orKey, setOrKey]         = useState('')

  const { data: models = [], isLoading: loadingModels } = useQuery({
    queryKey: ['models'],
    queryFn: fetchModels,
    retry: false,
  })

  const evalMutation = useMutation({
    mutationFn: (payload) => runEvaluation(payload),
  })

  const handleRun = () => {
    if (!prompt.trim() || selected.size === 0) return
    evalMutation.mutate({
      prompt,
      models: [...selected],
      criteria: [...criteria],
      api_keys: orKey ? { openrouter: orKey } : {},
    })
  }

  const running = evalMutation.isPending
  const result  = evalMutation.data
  const error   = evalMutation.error

  return (
    <div className={s.page}>
      {/* Header */}
      <div className={s.header}>
        <h1 className={s.title}>Evaluate Models</h1>
        <p className={s.sub}>Run your prompt across multiple AI models and get scored results</p>
      </div>

      {/* Config panel */}
      <div className={s.config}>
        {/* Prompt */}
        <div className={s.section}>
          <label className={s.label}>Prompt</label>
          <textarea
            className={s.promptInput}
            placeholder="Enter your prompt here… e.g. 'Explain quantum computing to a 10-year-old'"
            value={prompt}
            onChange={e => setPrompt(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter' && e.metaKey) handleRun() }}
            rows={4}
          />
        </div>

        {/* OpenRouter key */}
        <div className={s.section}>
          <label className={s.label}>OpenRouter API Key <span className={s.optional}>(or set in .env)</span></label>
          <input
            className={s.keyInput}
            type="password"
            placeholder="sk-or-v1-..."
            value={orKey}
            onChange={e => setOrKey(e.target.value)}
          />
        </div>

        <div className={s.twoCol}>
          {/* Model selector */}
          <div className={s.section}>
            <label className={s.label}>Models <span className={s.count}>({selected.size} selected)</span></label>
            <ModelSelector
              models={models}
              loading={loadingModels}
              selected={selected}
              onChange={setSelected}
            />
          </div>

          {/* Criteria selector */}
          <div className={s.section}>
            <label className={s.label}>Scoring Criteria</label>
            <CriteriaSelector criteria={criteria} onChange={setCriteria} />
          </div>
        </div>

        {/* Run button */}
        <div className={s.runRow}>
          {error && <span className={s.error}>⚠ {error.response?.data?.detail || error.message}</span>}
          <button
            className={s.runBtn}
            onClick={handleRun}
            disabled={running || !prompt.trim() || selected.size === 0}
          >
            {running
              ? `⏳ Evaluating ${selected.size} models…`
              : `▶ Run on ${selected.size} model${selected.size !== 1 ? 's' : ''}`}
          </button>
        </div>

        {/* Progress bar */}
        {running && <div className={s.progressBar}><div className={s.progressFill} /></div>}
      </div>

      {/* Results */}
      {result && <ResultsGrid result={result} />}
    </div>
  )
}
