<template>
  <div class="flex justify-center items-center min-h-screen bg-gray-100">
    <div class="bg-white p-6 rounded shadow-md w-full max-w-sm">
      <h2 class="text-xl font-bold mb-4 text-center">Register</h2>
      <form @submit.prevent="handleRegister">

        <div class="mb-4">
          <label>Email</label>
          <input v-model="email" type="email" required class="input" />
        </div>
        <div class="mb-4">
          <label>Password</label>
          <input v-model="password" type="password" required class="input" />
        </div>
        <div v-if="error" class="text-red-600 mb-2">{{ error }}</div>
        <button type="submit" class="btn">Register</button>
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

async function handleRegister() {
  error.value = null
  try {
    await axios.post('https://reqres.in/api/register', {
      
      email: email.value,
      password: password.value
    })
    localStorage.setItem('token', response.data.token)
    success.value = true

    // Simulate redirect after 2 seconds
    setTimeout(() => {
      router.push('/Login')
    }, 2000)
  } catch (err) {
    error.value = err.response?.data?.error || 'Registration failed'
  }
}
</script>

<style scoped>
.input {
  @apply w-full px-3 py-2 border rounded;
}
.btn {
  @apply w-full bg-green-600 text-white py-2 rounded hover:bg-green-700;
}
</style>
