import { Link } from 'react-router-dom'
import { Zap, Target, Map, BookOpen, Lightbulb, TrendingUp } from 'lucide-react'
import './Home.css'

const FEATURES = [
  { icon: <Lightbulb size={24} />, title: 'Lean Idea Architect', desc: 'Transform raw ideas into structured Lean Canvas in seconds' },
  { icon: <TrendingUp size={24} />, title: 'Business Modeler', desc: 'Generate complete Business Model Canvas automatically' },
  { icon: <Target size={24} />, title: 'OKR Strategist', desc: 'Define measurable objectives aligned to your product vision' },
  { icon: <Map size={24} />, title: 'Roadmap Planner', desc: 'Build phased outcome-driven roadmaps with dependencies' },
  { icon: <BookOpen size={24} />, title: 'User Story Teller', desc: 'Generate Jira-ready stories with Gherkin acceptance criteria' },
  { icon: <Zap size={24} />, title: 'Intent-Aware Routing', desc: 'AI orchestrator selects the right agent for your request' },
]

export default function Home() {
  return (
    <div className="home">
      {/* Hero */}
      <section className="hero">
        <div className="hero-content">
          <span className="badge badge-blue hero-badge">Powered by GPT-4o + LangGraph</span>
          <h1>From idea to Jira-ready execution — powered by Agentic AI</h1>
          <p>A multi-agent system that transforms product ideas into vision statements, roadmaps, OKRs, and sprint-ready user stories — eliminating weeks of manual work.</p>
          <div className="hero-actions">
            <Link to="/portal" className="btn btn-primary">Launch Portal</Link>
            <a href="https://github.com/sattringal1/gen-ai-product-manager" target="_blank" rel="noreferrer" className="btn btn-secondary">
              View on GitHub
            </a>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="features page">
        <div className="page-header">
          <h2 className="page-title">7 Specialist AI Agents</h2>
          <p className="page-subtitle">Each agent is a domain expert, orchestrated by an intent-aware router</p>
        </div>
        <div className="features-grid">
          {FEATURES.map((f, i) => (
            <div key={i} className="feature-card card">
              <div className="feature-icon">{f.icon}</div>
              <h3>{f.title}</h3>
              <p>{f.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Flow */}
      <section className="flow page">
        <h2 className="page-title" style={{ textAlign: 'center', marginBottom: 32 }}>How It Works</h2>
        <div className="flow-steps">
          {['Enter your product idea', 'Orchestrator routes to best agent', 'Agent generates structured output', 'Push to Jira / Confluence'].map((step, i) => (
            <div key={i} className="flow-step">
              <div className="flow-num">{i + 1}</div>
              <p>{step}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  )
}
