import axios from 'axios'

// 1. Create the Axios instance with the base URL from .env
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
})

// 2. Define our API calls
export default {
  // Health Check
  getHealth() {
    return api.get('/')
  },

  // Student CRUD
  getStudents() {
    return api.get('/students/')
  },
  createStudent(data) {
    return api.post('/students/', data)
  },
  updateStudent(id, data) {
    return api.put(`/students/${id}`, data)
  },
  deleteStudent(id) {
    return api.delete(`/students/${id}`)
  },
}
