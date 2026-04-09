import './AgentSelector.css'

export const AGENTS = [
  { id: 'lean_idea_architect',        label: 'Lean Idea Architect',   icon: '🧩', desc: 'Lean Canvas structure',       color: '#6366F1' },
  { id: 'business_modeler',           label: 'Business Modeler',      icon: '📊', desc: 'Business Model Canvas',       color: '#0EA5E9' },
  { id: 'value_proposition_designer', label: 'Value Proposition',     icon: '💎', desc: 'Customer needs mapping',      color: '#10B981' },
  { id: 'visionary',                  label: 'Visionary',             icon: '🔭', desc: 'Vision & mission statements', color: '#F59E0B' },
  { id: 'okr_strategist',             label: 'OKR Strategist',        icon: '🎯', desc: 'Objectives & Key Results',    color: '#EF4444' },
  { id: 'roadmap_planner',            label: 'Roadmap Planner',       icon: '🗺️', desc: 'Phased roadmap',             color: '#8B5CF6' },
  { id: 'user_story_teller',          label: 'User Story Teller',     icon: '📝', desc: 'Jira-ready user stories',    color: '#EC4899' },
]

export const AGENT_META = Object.fromEntries(AGENTS.map(a => [a.id, a]))

export default function AgentSelector({ selected, onChange }) {
  const allSelected = selected.length === AGENTS.length
  const someSelected = selected.length > 0 && !allSelected

  const toggleAll = () => onChange(allSelected ? [] : AGENTS.map(a => a.id))
  const toggle = (id) =>
    onChange(selected.includes(id) ? selected.filter(x => x !== id) : [...selected, id])

  return (
    <div className="agent-selector-multi">
      <div className="agent-select-header">
        <label className="select-all-label">
          <span className="custom-checkbox">
            <input
              type="checkbox"
              checked={allSelected}
              ref={el => { if (el) el.indeterminate = someSelected }}
              onChange={toggleAll}
            />
            <span className="checkmark" />
          </span>
          <span className="select-all-text">Select All Agents</span>
        </label>
        <span className="agent-count-pill">
          {selected.length} / {AGENTS.length} selected
        </span>
      </div>

      <div className="agent-grid">
        {AGENTS.map(a => {
          const isSelected = selected.includes(a.id)
          return (
            <label
              key={a.id}
              className={`agent-card-check ${isSelected ? 'selected' : ''}`}
              style={isSelected ? { '--ac': a.color } : {}}
            >
              <span className="custom-checkbox">
                <input
                  type="checkbox"
                  checked={isSelected}
                  onChange={() => toggle(a.id)}
                />
                <span className="checkmark" />
              </span>
              <span className="agent-icon-badge" style={{ background: isSelected ? a.color + '22' : '#F1F5F9' }}>
                {a.icon}
              </span>
              <div className="agent-info">
                <span className="agent-label">{a.label}</span>
                <span className="agent-desc">{a.desc}</span>
              </div>
              {isSelected && (
                <span className="selected-dot" style={{ background: a.color }} />
              )}
            </label>
          )
        })}
      </div>
    </div>
  )
}
