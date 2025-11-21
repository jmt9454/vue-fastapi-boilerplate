import apiClient from './apiClient'

export default {
  getStudents() {
    return apiClient.get('/students/')
  },
  createStudent(data) {
    return apiClient.post('/students/', data)
  },
  updateStudent(id, data) {
    return apiClient.put(`/students/${id}`, data)
  },
  deleteStudent(id) {
    return apiClient.delete(`/students/${id}`)
  },
}
