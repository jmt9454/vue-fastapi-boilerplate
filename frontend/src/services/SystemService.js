import apiClient from './apiClient'

export default {
  getHealth() {
    return apiClient.get('/')
  },
}
