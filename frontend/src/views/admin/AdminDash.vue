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
        <h2>Active Games</h2>
        <p>{{ activeGames }}</p>
      </div>
      <div class="card">
        <h2>Inactive Games</h2>
        <p>{{ inactiveGames }}</p>
      </div>
      <div class="card">
        <h2>Total Games</h2>
        <p>{{ totalGames }}</p>
      </div>
    </div>

    <div class="game-management">
      <h2>Manage Games</h2>
      <table class="game-table">
        <thead>
          <tr>
            <th>Game Name</th>
            <th>Active</th>
            <th>Max Sessions</th>
            <th>Bets per Session</th>
            <th>Difficulty</th>
            <th>Tags</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="game in games" :key="game.id">
            <td>{{ game.name }}</td>
            <td>
              <span :class="['status-badge', game.is_active ? 'active' : 'inactive']">
                {{ game.is_active ? 'Active' : 'Inactive' }}
              </span>
            </td>
            <td>{{ game.max_sessions_per_user }}</td>
            <td>{{ game.max_bets_per_session }}</td>
            <td>{{ game.difficulty || '--' }}</td>
            <td>{{ game.tags }}</td>
            <td>
              <div class="action-icons">
                <span @click="openGame(game.name)" class="action-icon" title="Game Page">🎮</span>
                <span @click="openDocs(game.name)" class="action-icon" title="Raw Page">📄</span>
                <span @click="openEditModal(game)" class="action-icon" title="Edit Control">⚙️</span>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <EditGameControl
      :show="showEditModal"
      :game="selectedGame"
      @close="closeEditModal"
      @saved="handleGameSaved"
    />
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'
import EditGameControl from '@/components/modals/EditGameControl.vue'

const totalUsers = ref(0)
const totalGames = ref(0)
const activeGames = ref(0)
const inactiveGames = ref(0)
const games = ref([])
const showEditModal = ref(false)
const selectedGame = ref(null)

onMounted(async () => {
  try {
    const gamesListResponse = await api.get('/admin/games')

    console.log('gamesListResponse:', gamesListResponse.data)

    if (gamesListResponse.data && Array.isArray(gamesListResponse.data.games)) {
      games.value = gamesListResponse.data.games

      activeGames.value = games.value.filter(g => g.is_active).length
      inactiveGames.value = games.value.filter(g => !g.is_active).length
      totalGames.value = activeGames.value + inactiveGames.value
    } else {
      console.error('Invalid games list response:', gamesListResponse.data)
    }
  } catch (error) {
    console.error('Error fetching data:', error)
  }
})


const openGame = (gameName) => {
  const baseUrl = window.location.origin
  window.open(`${baseUrl}/game/${gameName}`, '_blank')
}

const openDocs = (gameName) => {
  const baseUrl = window.location.origin
  window.open(`${baseUrl}/game/${gameName}/docs`, '_blank')
}

const openEditModal = (game) => {
  selectedGame.value = { ...game }
  showEditModal.value = true
}

const closeEditModal = () => {
  showEditModal.value = false
  selectedGame.value = null
}

const handleGameSaved = async () => {
  try {
    const gamesListResponse = await api.get('/admin/games')
    if (gamesListResponse.data && Array.isArray(gamesListResponse.data.games)) {
      games.value = gamesListResponse.data.games
      activeGames.value = games.value.filter(g => g.is_active).length
      inactiveGames.value = games.value.filter(g => !g.is_active).length
      totalGames.value = activeGames.value + inactiveGames.value
    }
  } catch (error) {
    console.error('Error refreshing games list:', error)
  }
}
</script>

<style scoped>
.admin-dashboard {
  padding: 20px;
}

.dashboard-cards {
  display: flex;
  gap: 20px;
  margin-bottom: 40px;
}

.card {
  background-color: white;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 5px;
  flex: 1;
}

.game-management {
  margin-top: 40px;
}

.game-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #2a2a2a;
  color: white;
}

.game-table th,
.game-table td {
  padding: 12px;
  border: 1px solid #484848;
  text-align: left;
}

.game-table th {
  background-color: #343434;
  font-weight: bold;
}

.status-badge {
  padding: 4px 8px;
  border-radius: 12px;
  font-size: 0.9em;
}

.status-badge.active {
  background-color: #4CAF50;
  color: white;
}

.status-badge.inactive {
  background-color: #666;
  color: white;
}

.action-icons {
  display: flex;
  gap: 5px;
  align-items: center;
}

.action-icon {
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: background-color 0.2s ease;
}

.action-icon:hover {
  background-color: #3a3a3a;
}
</style>
