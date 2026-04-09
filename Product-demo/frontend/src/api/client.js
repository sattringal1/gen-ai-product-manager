import axios from 'axios'

const api = axios.create({
  baseURL: '/api/v1',
  timeout: 120000, // LLM calls can be slow
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
  const { data } = await axios.get('/health')
  return data
}

export default api
