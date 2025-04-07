<template>
  <div class="player-dashboard">
    <h1>Player Dashboard</h1>
    <p>Welcome to your dashboard. Here you can view your stats and recent activities.</p>
    <div class="dashboard-cards">
      <div class="card">
        <h2>Your Games</h2>
        <p>{{ totalGames }}</p>
      </div>
      <div class="card">
        <h2>Your Achievements</h2>
        <p>{{ totalAchievements }}</p>
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

const totalGames = ref(0)
const totalAchievements = ref(0)
const recentActivities = ref([])

const fetchDashboardData = async () => {
  console.log("Fetching dashboard data")
}

onMounted(fetchDashboardData)
</script>

<style scoped>
.player-dashboard {
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
