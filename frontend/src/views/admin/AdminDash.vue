<template>
  <div class="admin-dashboard">
    <h1>Admin Dashboard</h1>
    <p>Welcome to the admin dashboard. Here you can manage your application.</p>
    <div class="dashboard-cards">
      <div class="card">
        <h2>Total Users</h2>
        <p>{{ totalUsers }}</p>
      </div>
      <div class="card">
        <h2>Total Games</h2>
        <p>{{ totalGames }}</p>
      </div>
      <div class="card">
        <h2>Recent Activities</h2>
        <ul>
          <li v-for="activity in recentActivities" :key="activity.id">{{ activity.description }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const totalUsers = ref(0)
const totalGames = ref(0)
const recentActivities = ref([])

const fetchDashboardData = async () => {
    console.log("Fetching dashboard data")
}

onMounted(fetchDashboardData)
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.dashboard-cards {
  display: flex;
  gap: 20px;
}

.card {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 5px;
  flex: 1;
}
</style>
