import ReactMarkdown from 'react-markdown'
import './ResultsDisplay.css'

const AGENT_LABELS = {
  lean_idea_architect: '🧩 Lean Canvas',
  business_modeler: '📊 Business Model Canvas',
  value_proposition_designer: '💎 Value Proposition',
  visionary: '🔭 Vision Statement',
  okr_strategist: '🎯 OKRs',
  roadmap_planner: '🗺️ Roadmap',
  user_story_teller: '📝 User Stories',
}

function JsonViewer({ data }) {
  if (!data) return null
  return (
    <pre className="json-viewer">
      {JSON.stringify(data, null, 2)}
    </pre>
  )
}

function UserStoriesView({ data }) {
  if (!data?.stories) return <JsonViewer data={data} />
  return (
    <div className="stories-view">
      <div className="epic-header">
        <h3>{data.epic_name}</h3>
        <p>{data.epic_summary}</p>
      </div>
      <div className="stories-grid">
        {data.stories.map((s, i) => (
          <div key={i} className="story-card">
            <div className="story-header">
              <span className={`badge badge-${priorityColor(s.priority)}`}>{s.priority}</span>
              <span className="story-points">{s.story_points} pts</span>
            </div>
            <h4>{s.title}</h4>
            <p className="story-body">
              As a <strong>{s.as_a}</strong>, I want <strong>{s.i_want}</strong>, so that <em>{s.so_that}</em>.
            </p>
            <div className="ac-list">
              <strong>Acceptance Criteria:</strong>
              {s.acceptance_criteria?.map((ac, j) => (
                <div key={j} className="ac-item">
                  <span className="ac-tag">GIVEN</span>{ac.given}&nbsp;
                  <span className="ac-tag">WHEN</span>{ac.when}&nbsp;
                  <span className="ac-tag">THEN</span>{ac.then}
                </div>
              ))}
            </div>
            {s.labels?.length > 0 && (
              <div className="story-labels">
                {s.labels.map((l, j) => <span key={j} className="badge badge-blue">{l}</span>)}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

function priorityColor(p) {
  return { Critical: 'red', High: 'orange', Medium: 'blue', Low: 'green' }[p] || 'blue'
}

export default function ResultsDisplay({ result }) {
  if (!result) return null
  const { agent, output, jira_issue_keys, confluence_page_url } = result
  const label = AGENT_LABELS[agent] || agent

  return (
    <div className="results">
      <div className="results-header">
        <h2>{label}</h2>
        <div className="results-meta">
          {jira_issue_keys?.length > 0 && (
            <span className="badge badge-green">
              Jira: {jira_issue_keys.join(', ')}
            </span>
          )}
          {confluence_page_url && (
            <a href={confluence_page_url} target="_blank" rel="noreferrer" className="badge badge-blue">
              Confluence Page ↗
            </a>
          )}
        </div>
      </div>
      <div className="results-body">
        {agent === 'user_story_teller'
          ? <UserStoriesView data={output} />
          : <JsonViewer data={output} />
        }
      </div>
    </div>
  )
}
