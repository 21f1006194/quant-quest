<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h2>Login</h2>
    <div class="text-center">
      <div id="g_id_onload"
        :data-client_id="googleClientId"
        data-context="signin"
        data-ux_mode="popup"
        data-callback="handleGoogleCredentialResponse"
        data-auto_prompt="false">
      </div>

      <div class="g_id_signin"
        data-type="standard"
        data-shape="rectangular"
        data-theme="outline"
        data-text="signin_with"
        data-size="large"
        data-logo_alignment="left">
      </div>

      <div class="mt-4 text-start">
        <h5 class="mb-3">Before You Begin:</h5>
        <ul class="list-unstyled mb-4">
          <li class="mb-2">📝 Complete your registration in the Paradox Portal first</li>
          <li class="mb-2">❓ Having trouble? <router-link to="/about">Get help here</router-link></li>
          <li class="mb-2">📋 Read our <a href="https://docs.google.com/document/d/1TmIwqLpoozXmOE0buaqYRjzGHYSew6Qa_zGOxNrLuWY/edit?tab=t.0" target="_blank">Rules & Guidelines</a></li>
        </ul>

        <div class="alert alert-warning bg-transparent border-warning text-warning">
          <i class="bi bi-exclamation-triangle-fill me-2"></i>
          <strong>Important:</strong> All participants must follow Paradox and event guidelines
        </div>

        <div class="alert alert-info bg-transparent border-info text-info">
          <i class="bi bi-emoji-smile me-2"></i>
          <p class="mb-0">Have fun and learn! Remember, the journey is as important as the destination.</p>
        </div>
      </div>
    </div>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/authStore'
import api from '@/services/api'

const error = ref('')
const router = useRouter()
const authStore = useAuthStore()
const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID

// Initialize Google Sign-In
onMounted(() => {
  // Load the Google Sign-In script
  const script = document.createElement('script')
  script.src = 'https://accounts.google.com/gsi/client'
  script.async = true
  script.defer = true
  document.head.appendChild(script)

  // Add the callback function to window object
  window.handleGoogleCredentialResponse = handleGoogleCredentialResponse
})

onUnmounted(() => {
  // Clean up the callback function
  delete window.handleGoogleCredentialResponse
})

const handleGoogleCredentialResponse = async (response) => {
  error.value = ''
  try {
    // Send credential to backend
    const authResponse = await api.post('/auth/google', {
      token: response.credential
    })

    // Use auth store to handle login
    authStore.login(authResponse.data)

    // Redirect to homepage
    if (authStore.isAdmin) {
      router.push('/admin')
    } else if (authStore.isUser) {
      router.push('/player')
    } else {
      error.value = 'Invalid user role'
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Authentication failed'
  }
}
</script>

<style scoped>
.g_id_signin {
  width: 100% !important;
  display: flex;
  justify-content: center;
}
</style>
