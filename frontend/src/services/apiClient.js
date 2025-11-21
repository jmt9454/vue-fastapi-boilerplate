import axios from 'axios'

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL, // Reads from .env
  headers: {
    'Content-Type': 'application/json',
  },
})

// Optional: Add interceptors for handling tokens automatically
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export default apiClient
