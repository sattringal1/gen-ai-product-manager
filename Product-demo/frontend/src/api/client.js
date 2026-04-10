import axios from 'axios'

// In production the backend URL is injected at container start into /config.js
// In development Vite proxies /api to localhost:8000
const getBaseURL = () => {
  if (window.__RUNTIME_CONFIG__?.BACKEND_URL) {
    return window.__RUNTIME_CONFIG__.BACKEND_URL + '/api/v1'
  }
  return '/api/v1'
}

const api = axios.create({
  baseURL: getBaseURL(),
  timeout: 120000,
  headers: { 'Content-Type': 'application/json' },
})

export const processIdea = async ({ idea, agent = 'auto', pushToJira = false, pushToConfluence = false, jiraProjectKey, confluenceSpaceKey }) => {
  const { data } = await api.post('/process', {
    idea,
    agent,
    push_to_jira: pushToJira,
    push_to_confluence: pushToConfluence,
    jira_project_key: jiraProjectKey || null,
    confluence_space_key: confluenceSpaceKey || null,
  })
  return data
}

export const getAgents = async () => {
  const { data } = await api.get('/agents')
  return data.agents
}

export const getHealth = async () => {
  const { data } = await api.get('/health')
  return data
}

export default api
