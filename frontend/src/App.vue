<script setup>
import { RouterView } from 'vue-router'
</script>

<template>
  <v-app>
    <!-- Navigation Bar -->
    <v-app-bar color="primary" elevation="2">
      <template v-slot:prepend>
        <v-app-bar-nav-icon icon="mdi-school"></v-app-bar-nav-icon>
      </template>

      <v-app-bar-title>University App</v-app-bar-title>

      <template v-slot:append>
        <v-btn to="/" class="mr-2">Home</v-btn>
        <v-btn to="/students" variant="outlined">Students</v-btn>
      </template>
    </v-app-bar>

    <!-- Main Content Area -->
    <v-main class="bg-grey-lighten-4">
      <RouterView />
    </v-main>
  </v-app>
</template>

<style>
/* Global Styles can go here */
</style>
