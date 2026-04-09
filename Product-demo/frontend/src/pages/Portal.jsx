import { useState } from 'react'
import AgentSelector from '../components/AgentSelector'
import ResultsDashboard from '../components/ResultsDashboard'
import { processIdea } from '../api/client'
import { Send, RefreshCw, Settings, Trash2 } from 'lucide-react'
import './Portal.css'

const EXAMPLES = [
  'A mobile app that helps remote teams track wellbeing and prevent burnout using AI-powered nudges',
  'A B2B SaaS platform that automates procurement for mid-market manufacturing companies',
  'An AI assistant for product managers that turns meeting notes into Jira tickets automatically',
]

const DEFAULT_AGENTS = ['lean_idea_architect', 'business_modeler', 'visionary', 'okr_strategist']

export default function Portal() {
  const [idea, setIdea] = useState('')
  const [selectedAgents, setSelectedAgents] = useState(DEFAULT_AGENTS)
  const [loading, setLoading] = useState(false)
  const [results, setResults] = useState([])
  const [agentStatuses, setAgentStatuses] = useState({})
  const [error, setError] = useState(null)
  const [showOptions, setShowOptions] = useState(false)
  const [pushToJira, setPushToJira] = useState(false)
  const [pushToConfluence, setPushToConfluence] = useState(false)
  const [submitted, setSubmitted] = useState(false)

  const runAgents = async (agentsToRun, currentIdea) => {
    setLoading(true)
    setError(null)
    setResults([])
    setSubmitted(true)

    const initialStatuses = {}
    agentsToRun.forEach(a => { initialStatuses[a] = 'running' })
    setAgentStatuses(initialStatuses)

    await Promise.allSettled(
      agentsToRun.map(async (agent) => {
        try {
          const data = await processIdea({ idea: currentIdea, agent, pushToJira, pushToConfluence })
          setAgentStatuses(prev => ({ ...prev, [agent]: 'done' }))
          setResults(prev => [...prev, { agent, ...data, status: 'done' }])
        } catch (err) {
          setAgentStatuses(prev => ({ ...prev, [agent]: 'error' }))
          setResults(prev => [...prev, { agent, status: 'error', error: err.response?.data?.detail || err.message }])
        }
      })
    )

    setLoading(false)
  }

  const handleSubmit = async (e) => {
    e?.preventDefault()
    if (!idea.trim() || selectedAgents.length === 0) return
    await runAgents(selectedAgents, idea)
  }

  const handleRegenerate = () => {
    if (!idea.trim() || selectedAgents.length === 0) return
    runAgents(selectedAgents, idea)
  }

  const handleClear = () => {
    setResults([])
    setAgentStatuses({})
    setSubmitted(false)
    setIdea('')
    setError(null)
  }

  return (
    <div className="page portal-wide">
      <div className="page-header">
        <h1 className="page-title">AI Product Manager Portal</h1>
        <p className="page-subtitle">Describe your product idea — select agents and generate a full strategy dashboard</p>
      </div>

      <form onSubmit={handleSubmit} className="portal-form card">

        {/* Idea input */}
        <div className="form-group">
          <label className="form-label">Your Product Idea</label>
          <textarea
            rows={4}
            value={idea}
            onChange={e => setIdea(e.target.value)}
            placeholder="Describe your product idea in as much detail as possible…"
            disabled={loading}
          />
          <div className="examples">
            <span className="examples-label">Try an example:</span>
            {EXAMPLES.map((ex, i) => (
              <button key={i} type="button" className="example-chip" onClick={() => setIdea(ex)} disabled={loading}>
                {ex.substring(0, 55)}…
              </button>
            ))}
          </div>
        </div>

        {/* Agent selector */}
        <div className="form-group">
          <label className="form-label">Select Agents to Run</label>
          <AgentSelector selected={selectedAgents} onChange={setSelectedAgents} />
          {selectedAgents.length === 0 && (
            <p className="form-hint">Select at least one agent to generate output.</p>
          )}
        </div>

        {/* Integration options */}
        <div className="form-group">
          <button type="button" className="options-toggle" onClick={() => setShowOptions(!showOptions)}>
            <Settings size={14} /> Integration Options {showOptions ? '▲' : '▼'}
          </button>
          {showOptions && (
            <div className="options-panel">
              <label className="checkbox-label">
                <input type="checkbox" checked={pushToJira} onChange={e => setPushToJira(e.target.checked)} />
                Push user stories to Jira
              </label>
              <label className="checkbox-label">
                <input type="checkbox" checked={pushToConfluence} onChange={e => setPushToConfluence(e.target.checked)} />
                Publish output to Confluence
              </label>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="form-actions">
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !idea.trim() || selectedAgents.length === 0}
          >
            {loading
              ? <><span className="spinner" style={{ width: 18, height: 18, borderWidth: 2 }} /> Running {selectedAgents.length} agent{selectedAgents.length !== 1 ? 's' : ''}…</>
              : <><Send size={16} /> Generate</>
            }
          </button>

          {submitted && !loading && (
            <button type="button" className="btn btn-secondary" onClick={handleRegenerate}>
              <RefreshCw size={15} /> Regenerate
            </button>
          )}

          {submitted && (
            <button type="button" className="btn btn-ghost" onClick={handleClear} disabled={loading}>
              <Trash2 size={15} /> Clear
            </button>
          )}
        </div>
      </form>

      {error && (
        <div className="error-banner card">
          <strong>Error:</strong> {error}
        </div>
      )}

      {submitted && (
        <ResultsDashboard
          results={results}
          agentStatuses={agentStatuses}
          selectedAgents={selectedAgents}
          idea={idea}
          loading={loading}
        />
      )}
    </div>
  )
}
