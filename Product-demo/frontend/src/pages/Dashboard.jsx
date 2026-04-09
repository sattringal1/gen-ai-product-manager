import { useEffect, useState } from 'react'
import { getHealth, getAgents } from '../api/client'
import { CheckCircle, XCircle, Cpu } from 'lucide-react'
import './Dashboard.css'

export default function Dashboard() {
  const [health, setHealth] = useState(null)
  const [agents, setAgents] = useState([])
  const [healthError, setHealthError] = useState(false)

  useEffect(() => {
    getHealth()
      .then(setHealth)
      .catch(() => setHealthError(true))
    getAgents().then(setAgents).catch(() => {})
  }, [])

  return (
    <div className="page dashboard">
      <div className="page-header">
        <h1 className="page-title">System Dashboard</h1>
        <p className="page-subtitle">Live status of all AI agents and integrations</p>
      </div>

      {/* Health card */}
      <div className="dash-section">
        <h2>Backend Health</h2>
        <div className="health-card card">
          {healthError ? (
            <div className="health-row">
              <XCircle size={20} color="var(--error)" />
              <span>Backend unreachable — is it running on port 8000?</span>
            </div>
          ) : health ? (
            <>
              <div className="health-row">
                <CheckCircle size={20} color="var(--success)" />
                <span>Status: <strong>{health.status}</strong></span>
              </div>
              <div className="health-row">
                <Cpu size={20} color="var(--primary)" />
                <span>LLM Provider: <strong>{health.llm_provider}</strong></span>
              </div>
              <div className="health-row">
                <span style={{width:20}} />
                <span>API Version: <strong>{health.version}</strong></span>
              </div>
            </>
          ) : (
            <div className="health-row"><div className="spinner" /> Checking...</div>
          )}
        </div>
      </div>

      {/* Agents */}
      <div className="dash-section">
        <h2>Available Agents</h2>
        <div className="agents-grid">
          {agents.map(a => (
            <div key={a.id} className="agent-status card">
              <div className="agent-status-header">
                <strong>{a.name}</strong>
                <span className="badge badge-green">Ready</span>
              </div>
              <p>{a.description}</p>
              <code className="agent-id">{a.id}</code>
            </div>
          ))}
        </div>
      </div>

      {/* Integration status */}
      <div className="dash-section">
        <h2>Integration Checklist</h2>
        <div className="checklist card">
          {[
            { label: 'OpenAI / Azure OpenAI API Key', env: 'OPENAI_API_KEY / AZURE_OPENAI_API_KEY' },
            { label: 'Jira Base URL + API Token', env: 'JIRA_BASE_URL, JIRA_API_TOKEN' },
            { label: 'Confluence Base URL + API Token', env: 'CONFLUENCE_BASE_URL, CONFLUENCE_API_TOKEN' },
          ].map((item, i) => (
            <div key={i} className="checklist-item">
              <span className="checklist-icon">⚙️</span>
              <div>
                <strong>{item.label}</strong>
                <p>Set <code>{item.env}</code> in <code>.env</code></p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
