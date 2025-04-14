<template>
  <div class="container mt-5" style="max-width: 400px;">
    <h2>Register</h2>
    <form @submit.prevent="register">
      <div class="mb-3">
        <label class="form-label">Email</label>
        <input v-model="email" type="email" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Username</label>
        <input v-model="username" type="text" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Password</label>
        <input v-model="password" type="password" class="form-control" required />
      </div>

      <div class="mb-3">
        <label class="form-label">Full Name</label>
        <input v-model="fullName" type="text" class="form-control" required />
      </div>

      <button type="submit" class="btn btn-primary w-100">Register</button>
    </form>

    <div v-if="error" class="alert alert-danger mt-3">{{ error }}</div>
    <div v-if="success" class="alert alert-success mt-3">
      Registration successful! Welcome, {{ fullName }} 
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const email = ref('')
const username = ref('')
const password = ref('')
const fullName = ref('')
const error = ref('')
const success = ref(false)
const name = ref('')  
const router = useRouter()

const register = async () => {
  error.value = ''
  success.value = false

  if (!fullName.value.trim()) {
    error.value = 'Full Name is required'
    return
  }

  try {
    const response = await api.post('/register', {
      email: email.value,
      username: username.value,
      password: password.value,
      full_name: fullName.value
    })

    const token = response.data.token
    localStorage.setItem('token', token)
    name.value = fullName.value
    success.value = true

    setTimeout(() => {
      router.push({ path: '/' })
    }, 2000)
  } catch (err) {
    console.error('Registration error:', err)
    error.value = err.response?.data?.error || 
                 err.message || 
                 'Registration failed'
  }
}
</script>
