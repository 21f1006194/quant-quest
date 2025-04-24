<template>
  <div class="game-wrapper">
    <div v-if="loading" class="loading">
      Loading game data...
    </div>
    <div v-else-if="!gameData?.is_active" class="game-inactive">
      <h2>Game Not Active</h2>
      <p>This game is currently not active. Please contact the administrator for more information.</p>
    </div>
    <router-view v-else :game-data="gameData"></router-view>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

defineOptions({
  name: 'GameWrapper'
})

const loading = ref(true)
const gameData = ref(null)

const fetchGameData = async () => {
  try {
    const response = await api.get('/game/ten_dice/info')
    gameData.value = response.data
  } catch (error) {
    console.error('Error fetching game data:', error)
  } finally {
    loading.value = false
  }
}

onMounted(fetchGameData)
</script>

<style scoped>
.game-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100%;
}

.game-page {
  width: 80%;
  margin: 0 auto;
}

.loading {
  font-size: 1.2rem;
  color: #666;
}

.game-inactive {
  text-align: center;
  padding: 2rem;
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
  border-radius: 4px;
  color: #856404;
}

.game-inactive h2 {
  margin-bottom: 1rem;
  color: #856404;
}
</style>