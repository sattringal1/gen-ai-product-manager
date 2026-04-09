import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { BrowserRouter } from 'react-router-dom'
import Portal from '../pages/Portal'

// Mock the API client
vi.mock('../api/client', () => ({
  processIdea: vi.fn(),
  getAgents: vi.fn(() => Promise.resolve([])),
}))

import { processIdea } from '../api/client'

const wrap = (ui) => <BrowserRouter>{ui}</BrowserRouter>

describe('Portal page', () => {
  beforeEach(() => { vi.clearAllMocks() })

  it('renders the idea textarea', () => {
    render(wrap(<Portal />))
    expect(screen.getByPlaceholderText(/describe your product idea/i)).toBeTruthy()
  })

  it('disables submit button when idea is empty', () => {
    render(wrap(<Portal />))
    const btn = screen.getByRole('button', { name: /generate/i })
    expect(btn).toBeDisabled()
  })

  it('enables submit button when idea is filled', async () => {
    render(wrap(<Portal />))
    const textarea = screen.getByPlaceholderText(/describe your product idea/i)
    await userEvent.type(textarea, 'An AI expense management app')
    const btn = screen.getByRole('button', { name: /generate/i })
    expect(btn).not.toBeDisabled()
  })

  it('calls processIdea on form submit', async () => {
    processIdea.mockResolvedValueOnce({
      agent: 'lean_idea_architect',
      idea: 'test idea',
      output: { problem: ['test'] },
      raw_text: '{}',
      jira_issue_keys: [],
    })
    render(wrap(<Portal />))
    await userEvent.type(screen.getByPlaceholderText(/describe your product idea/i), 'A product idea longer than ten chars')
    fireEvent.submit(screen.getByRole('button', { name: /generate/i }).closest('form'))
    await waitFor(() => expect(processIdea).toHaveBeenCalledTimes(1))
  })

  it('shows error message on API failure', async () => {
    processIdea.mockRejectedValueOnce({ message: 'Network error' })
    render(wrap(<Portal />))
    await userEvent.type(screen.getByPlaceholderText(/describe your product idea/i), 'A product idea')
    fireEvent.submit(screen.getByRole('button', { name: /generate/i }).closest('form'))
    await waitFor(() => expect(screen.getByText(/error/i)).toBeTruthy())
  })

  it('fills idea when clicking an example chip', async () => {
    render(wrap(<Portal />))
    const chips = screen.getAllByRole('button', { name: /\.\.\./i })
    await userEvent.click(chips[0])
    const textarea = screen.getByPlaceholderText(/describe your product idea/i)
    expect(textarea.value.length).toBeGreaterThan(0)
  })
})
