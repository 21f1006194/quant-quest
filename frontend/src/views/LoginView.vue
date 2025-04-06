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

      <button type="submit" class="btn btn-primary w-100">Login</button>
    </form>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/authStore'
import api from '@/services/api' 

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()
const authStore = useAuthStore()

const handleLogin = async () => {
  error.value = ''
  try {
    const response = await api.post('/login', {
      username: username.value,
      password: password.value
    })

    // Use auth store to handle login
    authStore.login(response.data.token, response.data.user)

    // Redirect to homepage
    router.push('/')
  } catch (err) {
    error.value = err.response?.data?.error || 'Login failed'
  }
}
</script>
