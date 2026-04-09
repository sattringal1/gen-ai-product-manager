import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent } from '@testing-library/react'
import AgentSelector from '../components/AgentSelector'

describe('AgentSelector', () => {
  it('renders all 8 agent options', () => {
    render(<AgentSelector value="auto" onChange={() => {}} />)
    expect(screen.getByText('Auto (AI decides)')).toBeTruthy()
    expect(screen.getByText('Lean Idea Architect')).toBeTruthy()
    expect(screen.getByText('User Story Teller')).toBeTruthy()
  })

  it('highlights selected agent', () => {
    render(<AgentSelector value="visionary" onChange={() => {}} />)
    const cards = document.querySelectorAll('.agent-card')
    const selected = Array.from(cards).find(c => c.classList.contains('selected'))
    expect(selected).toBeTruthy()
    expect(selected.textContent).toContain('Visionary')
  })

  it('calls onChange when an agent is clicked', () => {
    const onChange = vi.fn()
    render(<AgentSelector value="auto" onChange={onChange} />)
    fireEvent.click(screen.getByText('OKR Strategist').closest('.agent-card'))
    expect(onChange).toHaveBeenCalledWith('okr_strategist')
  })
})
