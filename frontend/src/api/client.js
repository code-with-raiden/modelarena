import axios from 'axios'

const client = axios.create({
  baseURL: '/api',
  headers: { 'Content-Type': 'application/json' },
  timeout: 120000,
})

export const fetchModels = () =>
  client.get('/models/').then(r => r.data.models)

export const runEvaluation = (payload) =>
  client.post('/evaluate/', payload).then(r => r.data)

export default client
