<template>
  <div class="flex items-center justify-center min-h-screen bg-gray-100">
    <div class="bg-white p-8 rounded shadow-md w-full max-w-sm">
      <h2 class="text-2xl font-bold mb-6 text-center">Login</h2>
      <form @submit.prevent="handleLogin">
        <div class="mb-4">
          <label class="block mb-1 font-semibold">Email</label>
          <input
            type="email"
            v-model="email"
            required
            class="w-full px-3 py-2 border rounded"
          />
        </div>
        <div class="mb-4">
          <label class="block mb-1 font-semibold">Password</label>
          <input
            type="password"
            v-model="password"
            required
            class="w-full px-3 py-2 border rounded"
          />
        </div>
        <button
          type="submit"
          class="w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700"
        >
          Login
        </button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'

const email = ref('')
const password = ref('')
const error = ref(null)
const router = useRouter()

async function handleLogin() {
  error.value = null
  try {
    const res = await axios.post('https://your-api.com/api/login', {
      email: email.value,
      password: password.value
    })
    localStorage.setItem('token', res.data.token)
    router.push('/') // Redirect to homepage or dashboard
  } catch (err) {
    error.value = err.response?.data?.message || 'Login failed'
  }
}
</script>

<style scoped>
.input {
  @apply w-full px-3 py-2 border rounded;
}
.btn {
  @apply w-full bg-blue-600 text-white py-2 rounded hover:bg-blue-700;
}
</style>
