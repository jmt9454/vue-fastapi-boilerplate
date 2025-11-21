<script setup>
import { ref } from 'vue'
import api from '../services/api'

const status = ref('Waiting for check...')
const isOnline = ref(false)
const isLoading = ref(false)

const checkApi = async () => {
  isLoading.value = true
  try {
    const response = await api.getHealth()
    status.value = response.data.message
    isOnline.value = true
  } catch (error) {
    status.value = 'Error: Backend is offline!'
    isOnline.value = false
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <v-container class="fill-height justify-center">
    <v-card class="text-center pa-6" elevation="4" min-width="400">
      <v-icon
        icon="mdi-server-network"
        size="64"
        :color="isOnline ? 'success' : 'grey'"
        class="mb-4"
      ></v-icon>

      <h1 class="text-h4 mb-2">System Status</h1>

      <v-alert :type="isOnline ? 'success' : 'warning'" variant="tonal" class="mb-6">
        {{ status }}
      </v-alert>

      <v-btn color="primary" size="large" :loading="isLoading" @click="checkApi">
        Check Connection
      </v-btn>
    </v-card>
  </v-container>
</template>
