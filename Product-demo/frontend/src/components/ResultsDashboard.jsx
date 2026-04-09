import { useRef } from 'react'
import { FileText, Download, CheckCircle, XCircle, Loader } from 'lucide-react'
import { AGENTS, AGENT_META } from './AgentSelector'
import './ResultsDashboard.css'

/* ─────────────────────────────────────────────
   Helpers
───────────────────────────────────────────── */
function formatKey(key) {
  return key.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase())
}

function flattenForExport(output, result = []) {
  if (!output || typeof output !== 'object') return result
  Object.entries(output).forEach(([k, v]) => {
    if (typeof v === 'string') {
      result.push({ key: formatKey(k), value: v })
    } else if (Array.isArray(v)) {
      result.push({ key: formatKey(k), value: v.map(i => (typeof i === 'string' ? i : JSON.stringify(i))).join(' • ') })
    } else if (typeof v === 'object' && v !== null) {
      flattenForExport(v, result)
    }
  })
  return result
}

/* ─────────────────────────────────────────────
   Output renderers
───────────────────────────────────────────── */
function ValueRenderer({ value }) {
  if (Array.isArray(value)) {
    return (
      <ul className="output-list">
        {value.map((item, i) => (
          <li key={i}>
            {typeof item === 'object' ? <StructuredOutput data={item} depth={1} /> : String(item)}
          </li>
        ))}
      </ul>
    )
  }
  if (typeof value === 'object' && value !== null) {
    return <StructuredOutput data={value} depth={1} />
  }
  return <p className="output-text">{String(value)}</p>
}

function StructuredOutput({ data, depth = 0 }) {
  if (!data || typeof data !== 'object') return <p className="output-text">{String(data)}</p>
  return (
    <div className={`structured-output depth-${depth}`}>
      {Object.entries(data).map(([key, value]) => (
        <div key={key} className="output-field">
          <span className="field-key">{formatKey(key)}</span>
          <ValueRenderer value={value} />
        </div>
      ))}
    </div>
  )
}

function UserStoriesOutput({ data }) {
  const priorityColor = p => ({ Critical: 'red', High: 'orange', Medium: 'blue', Low: 'green' }[p] || 'blue')
  return (
    <div className="stories-output">
      <div className="epic-banner">
        <strong>{data.epic_name}</strong>
        <p>{data.epic_summary}</p>
      </div>
      <div className="stories-mini-grid">
        {data.stories?.map((s, i) => (
          <div key={i} className="story-mini-card">
            <div className="story-mini-header">
              <span className={`badge badge-${priorityColor(s.priority)}`}>{s.priority}</span>
              <span className="pts-badge">{s.story_points} pt</span>
            </div>
            <strong className="story-title">{s.title}</strong>
            <p className="story-as">As a <em>{s.as_a}</em>, I want <em>{s.i_want}</em>.</p>
          </div>
        ))}
      </div>
    </div>
  )
}

function AgentOutput({ agent, output }) {
  if (!output) return <p className="no-output">No output returned.</p>
  if (agent === 'user_story_teller' && output.stories) return <UserStoriesOutput data={output} />
  return <StructuredOutput data={output} />
}

/* ─────────────────────────────────────────────
   Status indicators
───────────────────────────────────────────── */
function StatusIcon({ status }) {
  if (status === 'done')    return <CheckCircle size={14} className="si-done" />
  if (status === 'error')   return <XCircle size={14} className="si-error" />
  if (status === 'running') return <Loader size={14} className="si-running spin" />
  return null
}

/* ─────────────────────────────────────────────
   PDF export
───────────────────────────────────────────── */
async function exportToPDF(ref) {
  const { default: jsPDF } = await import('jspdf')
  const { default: html2canvas } = await import('html2canvas')

  const el = ref.current
  const canvas = await html2canvas(el, {
    scale: 1.5,
    useCORS: true,
    backgroundColor: '#F8FAFC',
    logging: false,
  })

  const imgW = canvas.width / 1.5
  const imgH = canvas.height / 1.5
  const pdf = new jsPDF({ orientation: imgW > imgH ? 'landscape' : 'portrait', unit: 'px', format: [imgW, imgH] })
  pdf.addImage(canvas.toDataURL('image/png'), 'PNG', 0, 0, imgW, imgH)
  pdf.save('ai-product-manager-report.pdf')
}

/* ─────────────────────────────────────────────
   PowerPoint export
───────────────────────────────────────────── */
async function exportToPPT(results, idea) {
  const { default: PptxGenJS } = await import('pptxgenjs')
  const pptx = new PptxGenJS()
  pptx.layout = 'LAYOUT_WIDE'
  pptx.author = 'Gen-AI Product Manager'

  /* Title slide */
  const ts = pptx.addSlide()
  ts.background = { color: '1E3A5F' }
  ts.addText('AI Product Manager Report', {
    x: 0.5, y: 1.8, w: 11.5, h: 1.2,
    fontSize: 38, bold: true, color: 'FFFFFF', align: 'center',
  })
  ts.addText(idea.substring(0, 160), {
    x: 1, y: 3.2, w: 10, h: 1.4,
    fontSize: 15, color: 'A5C8FF', align: 'center', italic: true,
  })
  ts.addText(new Date().toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' }), {
    x: 1, y: 5.2, w: 10, h: 0.5,
    fontSize: 11, color: '7AAAD4', align: 'center',
  })

  /* One slide per successful agent */
  results.filter(r => r.status === 'done').forEach(r => {
    const meta = AGENT_META[r.agent] || { label: r.agent, icon: '📄', color: '#2A6BD6' }
    const hexColor = (meta.color || '#2A6BD6').replace('#', '')
    const slide = pptx.addSlide()

    /* Header bar */
    slide.addShape(pptx.ShapeType.rect, { x: 0, y: 0, w: '100%', h: 1.1, fill: { color: hexColor } })
    slide.addText(`${meta.icon}  ${meta.label}`, {
      x: 0.4, y: 0.15, w: 11.5, h: 0.8,
      fontSize: 22, bold: true, color: 'FFFFFF',
    })

    /* Content rows */
    const fields = flattenForExport(r.output)
    let y = 1.35
    fields.slice(0, 7).forEach(({ key, value }) => {
      if (y > 6.8) return
      slide.addText(key, { x: 0.4, y, w: 11.5, h: 0.3, fontSize: 10, bold: true, color: '334155' })
      slide.addText(value.substring(0, 350), {
        x: 0.4, y: y + 0.3, w: 11.5, h: 0.55,
        fontSize: 10, color: '64748B',
      })
      y += 1.0
    })

    /* Footer */
    slide.addText('Generated by Gen-AI Product Manager', {
      x: 0, y: 7.1, w: '100%', h: 0.3,
      fontSize: 8, color: 'CBD5E1', align: 'center',
    })
  })

  pptx.writeFile({ fileName: 'ai-product-manager-report.pptx' })
}

/* ─────────────────────────────────────────────
   Main component
───────────────────────────────────────────── */
export default function ResultsDashboard({ results, agentStatuses, selectedAgents, idea, loading }) {
  const gridRef = useRef(null)

  const doneCount  = Object.values(agentStatuses).filter(s => s === 'done').length
  const total      = selectedAgents.length
  const progressPct = total > 0 ? Math.round((doneCount / total) * 100) : 0
  const hasResults  = results.filter(r => r.status === 'done').length > 0

  return (
    <div className="results-dashboard">

      {/* ── Status header ── */}
      <div className="dashboard-status-bar card">
        <div className="status-bar-top">
          <div className="status-bar-left">
            <h2 className="dash-title">Results Dashboard</h2>
            {loading && (
              <span className="running-label">
                <span className="spinner" style={{ width: 14, height: 14, borderWidth: 2 }} />
                Running {total - doneCount} agent{total - doneCount !== 1 ? 's' : ''}…
              </span>
            )}
          </div>
          {!loading && hasResults && (
            <div className="export-group">
              <button className="btn btn-export" onClick={() => exportToPDF(gridRef)}>
                <FileText size={14} /> Export PDF
              </button>
              <button className="btn btn-export-ppt" onClick={() => exportToPPT(results, idea)}>
                <Download size={14} /> Export PowerPoint
              </button>
            </div>
          )}
        </div>

        {loading && (
          <div className="progress-wrap">
            <div className="progress-track">
              <div className="progress-fill" style={{ width: `${progressPct}%` }} />
            </div>
            <span className="progress-text">{doneCount} / {total} complete</span>
          </div>
        )}

        <div className="agent-pill-row">
          {selectedAgents.map(id => {
            const meta   = AGENT_META[id] || { label: id, icon: '📄', color: '#64748B' }
            const status = agentStatuses[id] || 'queued'
            return (
              <div key={id} className={`agent-pill ${status}`} style={{ '--pc': meta.color }}>
                <span>{meta.icon}</span>
                <span className="pill-label">{meta.label}</span>
                <StatusIcon status={status} />
              </div>
            )
          })}
        </div>
      </div>

      {/* ── Results grid ── */}
      <div className="dashboard-grid" ref={gridRef}>

        {/* Completed / errored results */}
        {results.map((r, i) => {
          const meta = AGENT_META[r.agent] || { label: r.agent, icon: '📄', color: '#2A6BD6', desc: '' }
          return (
            <div key={i} className="result-card card" style={{ '--rc': meta.color }}>
              <div className="result-card-header">
                <div className="rc-title-group">
                  <span className="rc-icon-wrap" style={{ background: meta.color + '22' }}>
                    {meta.icon}
                  </span>
                  <div>
                    <h3 className="rc-title">{meta.label}</h3>
                    <span className="rc-desc">{meta.desc}</span>
                  </div>
                </div>
                <div className="rc-badges">
                  {r.jira_issue_keys?.length > 0 && (
                    <span className="badge badge-green">Jira: {r.jira_issue_keys.join(', ')}</span>
                  )}
                  {r.confluence_page_url && (
                    <a href={r.confluence_page_url} target="_blank" rel="noreferrer" className="badge badge-blue">
                      Confluence ↗
                    </a>
                  )}
                </div>
              </div>
              <div className="result-card-body">
                {r.status === 'error'
                  ? <p className="error-text">⚠️ {r.error}</p>
                  : <AgentOutput agent={r.agent} output={r.output} />
                }
              </div>
            </div>
          )
        })}

        {/* Skeleton cards for still-running agents */}
        {loading && selectedAgents
          .filter(id => !results.find(r => r.agent === id))
          .map(id => {
            const meta = AGENT_META[id] || { label: id, icon: '📄', color: '#94A3B8', desc: '' }
            return (
              <div key={id} className="result-card card skeleton-card" style={{ '--rc': meta.color }}>
                <div className="result-card-header">
                  <div className="rc-title-group">
                    <span className="rc-icon-wrap" style={{ background: meta.color + '22' }}>{meta.icon}</span>
                    <div>
                      <h3 className="rc-title">{meta.label}</h3>
                      <span className="rc-desc">{meta.desc}</span>
                    </div>
                  </div>
                  <span className="skeleton-running-badge">
                    <Loader size={12} className="spin" /> Processing…
                  </span>
                </div>
                <div className="result-card-body">
                  <div className="skeleton-lines">
                    {[80, 60, 90, 55, 75, 45].map((w, i) => (
                      <div key={i} className="skel-line" style={{ width: `${w}%` }} />
                    ))}
                  </div>
                </div>
              </div>
            )
          })
        }
      </div>
    </div>
  )
}
