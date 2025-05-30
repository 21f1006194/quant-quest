<template>
  <div class="player-dashboard-layout">
        <div class="dashboard-column info-column">
      <div class="wallet-summary">
        <h2>Wallet Summary</h2>
        <div class="wallet-card">
          <span><img :src="CoinIcon" class="coin-icon" alt="coin" /> {{ balance }}</span>
          <div class="wallet-timestamp">{{ timestamp }}</div>
        </div>
      </div>
      <div class="transactions-section">
        <h2>Bonus & Penalties</h2>
        <div class="transactions-grid">
          <div v-for="transaction in transactions" 
               :key="transaction.id" 
               :class="['transaction-card', transaction.type]">
            <div class="transaction-amount">
              {{ transaction.type === 'credit' ? '+' : '-' }}{{ transaction.amount }}
            </div>
            <div class="transaction-details">
              <div class="transaction-category">
                <i v-if="transaction.category === 'penalty'" class="bi bi-exclamation-triangle-fill"></i>
                <i v-else-if="transaction.category === 'bonus'" class="bi bi-gift"></i>
                <span v-else>{{ transaction.category }}</span>
              </div>
              <div class="transaction-description">{{ transaction.description }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div class="dashboard-column games-column">
      <div class="games-section">
        <h2>Games</h2>
        <div class="games-grid">
          <div v-for="game in games" 
               :key="game.game_id" 
               class="game-card">
            <div class="game-header">
              <div class="game-name">{{ game.name.replace(/_/g, ' ').split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ') }}</div>
              <div class="game-difficulty">{{ game.difficulty }}</div>
            </div>
            <div class="game-stats">
              <div class="stat">
                <i class="bi bi-controller"></i>
                <div class="progress-container">
                  <div class="progress-bar" :style="{ width: `${((game.max_sessions_per_user - gameStore.gameSessionsCount.get(game.game_id)) / game.max_sessions_per_user) * 100}%` }"></div>
                  <span class="progress-text">{{ game.max_sessions_per_user - gameStore.gameSessionsCount.get(game.game_id) }} / {{ game.max_sessions_per_user }}</span>
                </div>
              </div>
              <div class="stat">
                <img :src="CoinIcon" class="coin-icon" alt="coin" />
                <span class="value" :class="{ 'positive': gameStore.gamePnls.get(game.game_id) > 0, 'negative': gameStore.gamePnls.get(game.game_id) < 0 }">
                  {{ gameStore.gamePnls.get(game.game_id) }}
                </span>
              </div>
            </div>
            <router-link :to="`/game/${game.name}`" class="play-button">
              <i class="bi bi-play-btn-fill"></i> Play
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed, ref } from 'vue';
import { useWalletStore } from '@/store/walletStore';
import { useGameStore } from '@/store/gameStore';
import api from '@/services/api';
import CoinIcon from '@/assets/coins-solid.svg';

const walletStore = useWalletStore();
const gameStore = useGameStore();
const games = computed(() => gameStore.games);

const balance = computed(() => walletStore.balance);
const timestamp = computed(() => walletStore.timestamp);
const transactions = computed(() => walletStore.transactions);

const fetchGames = async () => {
    try {
        const response = await api.get('/games');
        if (response.status === 200) {
            gameStore.initializeGames(response.data.games);
            console.log('Games fetched:', response.data.games);
        }
    } catch (error) {
        console.error('Error fetching games:', error);
    }
};

onMounted(async () => {
  console.log('PlayerDash mounted! Fetching transactions...');
  try {
    const response = await api.get('/transactions');
    console.log('Transactions response:', response.data);
    walletStore.setTransactions(response.data.transactions);
  } catch (error) {
    console.error('Error fetching transactions:', error);
  }
  await fetchGames();
  walletStore.initializeSSE();
  gameStore.initializeSSE();
});
</script>

<style scoped>
.player-dashboard-layout {
  display: flex;
  height: calc(100vh - 70px);
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
}

.dashboard-column {
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
  overflow-y: auto;
}

.games-column {
  flex: 2;
  min-width: 0;
}

.info-column {
  flex: 1;
  min-width: 300px;
  max-width: 400px;
}

.games-section {
  margin-bottom: 30px;
}

.games-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 15px;
  margin-top: 15px;
}

.game-card {
  background-color: #343434;
  padding: 15px;
  border-radius: 8px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
  border: 1px solid #484848;
}

.game-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.game-name {
  font-weight: bold;
  font-size: 1.1em;
  color: #fff;
}

.game-difficulty {
  font-size: 0.9em;
  color: #888;
  padding: 2px 8px;
  background-color: #484848;
  border-radius: 4px;
}

.game-stats {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.stat {
  display: flex;
  justify-content: space-between;
  font-size: 0.9em;
  align-items: center;
}

.stat i {
  color: #888;
  font-size: 1.1em;
  margin-right: 8px;
}

.stat .value {
  font-weight: bold;
}

.stat .value.positive {
  color: #00ff00;
}

.stat .value.negative {
  color: #ff0000;
}

.play-button {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
  background-color: #484848;
  color: #fff;
  padding: 8px;
  border-radius: 4px;
  text-decoration: none;
  transition: background-color 0.2s;
}

.play-button:hover {
  background-color: #585858;
}

.play-button i {
  font-size: 1.1em;
}

.wallet-summary {
  margin-bottom: 30px;
}

.wallet-card {
  background-color: #343434;
  padding: 15px 25px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
  min-width: 200px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #484848;
}

.wallet-card i {
  color: #00ff00;
  font-size: 1.2em;
  margin-right: 8px;
}

.coin-icon {
  width: 1.2em;
  height: 1.2em;
  margin-right: 8px;
  filter: invert(1);
}

.wallet-card span {
  font-size: 1.5em;
  font-weight: bold;
  color: #fff;
  display: flex;
  align-items: center;
}

.stat .coin-icon {
  width: 1.1em;
  height: 1.1em;
  margin-right: 8px;
  filter: invert(1);
}

.wallet-timestamp {
  color: #888;
  font-size: 0.8em;
}

.transactions-section {
  margin-bottom: 30px;
}

.transactions-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  margin-top: 15px;
}

.transaction-card {
  padding: 7px 12px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  gap: 10px;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.08);
  min-height: 36px;
}

.transaction-card.credit {
  background-color: rgba(0, 255, 0, 0.08);
  border: 1px solid rgba(0, 255, 0, 0.18);
}

.transaction-card.debit {
  background-color: rgba(255, 0, 0, 0.08);
  border: 1px solid rgba(255, 0, 0, 0.18);
}

.transaction-amount {
  font-size: 1em;
  font-weight: bold;
}

.transaction-card.credit .transaction-amount {
  color: #00ff00;
}

.transaction-card.debit .transaction-amount {
  color: #ff0000;
}

.transaction-details {
  flex: 1;
}

.transaction-category {
  font-size: 0.95em;
  display: flex;
  align-items: center;
}

.transaction-category i {
  font-size: 1.1em;
  margin-right: 4px;
}

.transaction-category i.bi-exclamation-triangle-fill {
  color: #ff6b6b;
}

.transaction-category i.bi-gift {
  color: #4ecdc4;
}

.transaction-description {
  font-size: 0.85em;
  color: #666;
}

.progress-container {
  position: relative;
  width: 100%;
  height: 8px;
  background-color: #484848;
  border-radius: 4px;
  overflow: hidden;
}

.progress-bar {
  height: 100%;
  background-color: #00ff00;
  transition: width 0.3s ease;
}

.progress-text {
  position: absolute;
  right: 0;
  top: -20px;
  font-size: 0.8em;
  color: #888;
}

@media (max-width: 1100px) {
  .player-dashboard-layout {
    flex-direction: column;
    height: auto;
  }
  
  .dashboard-column {
    max-width: 100% !important;
    min-width: 0;
    height: auto;
    margin-bottom: 30px;
  }
  
  .info-column {
    max-width: 100% !important;
  }
}
</style>
