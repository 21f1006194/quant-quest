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
        <GameToggle v-for="game in games" :key="game.id" :gameId="game.id" :gameName="game.name"
          :isActive="game.isActive" @toggle="handleGameToggle" />
      </div>
      <div class="card">
        <h2>Game Scores</h2>
        <ul>
          <li v-for="score in gameScores" :key="score.gameId">
            {{ score.gameName }}: {{ score.score }}
          </li>
        </ul>
      </div>
      <div class="card">
        <h2>Rate Limits</h2>
        <ul>
          <li v-for="limit in rateLimits" :key="limit.id">
            {{ limit.name }}: {{ limit.value }}
            <button @click="updateRateLimit(limit.id)">Update</button>
          </li>
        </ul>
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
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import GameToggle from '@/components/GameToggle.vue';

const totalUsers = ref(0);
const totalGames = ref(0);
const recentActivities = ref([]);
const games = ref([]);
const gameScores = ref([]);
const rateLimits = ref([]);

const fetchDashboardData = async () => {
  try {
    const response = await api.get('/admin/dashboard');
    totalUsers.value = response.data.totalUsers;
    totalGames.value = response.data.totalGames;
    recentActivities.value = response.data.recentActivities;
    games.value = response.data.games;
    gameScores.value = response.data.gameScores;
    rateLimits.value = response.data.rateLimits;
  } catch (error) {
    console.error('Error fetching dashboard data:', error);
  }
};

const handleGameToggle = async ({ gameId, isActive }) => {
  try {
    await api.post(`/admin/games/${gameId}/toggle`, { isActive });
    const game = games.value.find((g) => g.id === gameId);
    if (game) game.isActive = isActive;
  } catch (error) {
    console.error('Error toggling game status:', error);
  }
};

const updateRateLimit = async (id) => {
  try {
    const newValue = prompt('Enter new rate limit value:');
    if (newValue) {
      await api.post(`/admin/rate-limits/${id}`, { value: newValue });
      const limit = rateLimits.value.find((l) => l.id === id);
      if (limit) limit.value = newValue;
    }
  } catch (error) {
    console.error('Error updating rate limit:', error);
  }
};

onMounted(fetchDashboardData);
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.dashboard-cards {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.card {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 5px;
  flex: 1;
  min-width: 300px;
}
</style>
