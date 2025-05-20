<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h2>Login</h2>
    <form @submit.prevent="handleLogin">
      <div class="mb-3">
        <label class="form-label">Username</label>
        <input v-model="username" type="text" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>

      <button type="submit" class="btn btn-primary w-100 mb-3">Login</button>
      
      <div class="text-center">
        <p class="text-muted">- OR -</p>
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
      </div>
    </form>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/authStore'
import api from '@/services/api'

const username = ref('')
const password = ref('')
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

const handleLogin = async () => {
  error.value = ''
  try {
    const response = await api.post('/login', {
      username: username.value,
      password: password.value
    })

    // Use auth store to handle login
    authStore.login(response.data)

    // Redirect to homepage
    if (authStore.isAdmin) {
      router.push('/admin')
    } else if (authStore.isUser) {
      router.push('/player')
    } else {
      error.value = 'Invalid user role'
    }
  } catch (err) {
    error.value = err.response?.data?.error || 'Login failed'
  }
}

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
