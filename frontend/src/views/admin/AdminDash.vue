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
            <th>Max sessions per user</th>
            <th>Max bets per session</th>
            <th>Max bet amount</th>
            <th>Min bet amount</th>
            <th>Payout</th>
            <th>Save</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="game in games" :key="game.id">
            <td>{{ game.name }}</td>
            <td>
              <input type="checkbox" v-model="game.is_active" />
            </td>
            <td>
              <input type="number" v-model.number="game.max_sessions_per_user" min="1" class="wide-input" />
            </td>
            <td>
              <input type="number" v-model.number="game.max_bets_per_session" min="1" />
            </td>
            <td>
              <input type="number" v-model.number="game.config_data.max_bet_amount" min="1" />
            </td>
            <td>
              <input type="number" v-model.number="game.config_data.min_bet_amount" min="1" />
            </td>
            <td>
              <input type="number" v-model.number="game.config_data.payout" min="1" />
            </td>



            <td>
              <button @click="saveGameSettings(game)">Save</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import api from '@/services/api'

const totalUsers = ref(0)
const totalGames = ref(0)
const activeGames = ref(0)
const inactiveGames = ref(0)
const games = ref([])

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

const saveGameSettings = async (game) => {
  try {
    const encodedName = encodeURIComponent(game.name);
    await api.post(`/game/${encodedName}/control`, {
      is_active: game.is_active,
      max_sessions_per_user: game.max_sessions_per_user,
      max_bets_per_session: game.max_bets_per_session,
      config: {
        max_bet_amount: game.config_data.max_bet_amount,
        min_bet_amount: game.config_data.min_bet_amount,
        payout: game.config_data.payout
      }

    })
    alert(`Settings saved for ${game.name}!`);
  } catch (error) {
    console.error('Error saving game settings:', error.response?.data || error.message);
    alert(`Failed to save settings for ${game.name}`);
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
}

.game-table th,
.game-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

button {
  padding: 5px 10px;
  background-color: #4CAF50;
  border: none;
  color: white;
  border-radius: 4px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

input[type="number"] {
  width: 60px;
}

/* Make this more specific to override the general input[type="number"] rule */
input[type="number"].wide-input {
    width: 150px;
    padding: 8px;
    border: 1px solid #484848;
    border-radius: 4px;
    background-color: #343434;
    color: white;
}

.wide-input:focus {
    outline: none;
    border-color: #00ff00;
}
</style>
