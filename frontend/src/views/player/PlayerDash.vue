<template>
  <div class="player-dashboard-layout">
    <div class="dashboard-column wallet-column">
      <div class="wallet-summary">
        <h2>Wallet Summary</h2>
        <div class="wallet-card">
          <span><i class="bi bi-wallet2"></i> {{ balance }}</span>
          <div class="wallet-timestamp">  {{ timestamp }}</div>
        </div>
      </div>
    </div>
    <!-- <div class="dashboard-column gamepnl-column">
      <div class="game-pnl-section">
        <h2>Game Performance</h2>
        <div class="game-pnl-grid">
          <div v-for="(pnl, gameId) in gamePnls" 
               :key="gameId" 
               class="game-pnl-card">
            <div class="game-pnl-row">
              <div class="game-name">Game {{ gameId }}</div>
              <div class="pnl-value" :class="{ 'positive': pnl > 0, 'negative': pnl < 0 }">
                {{ pnl > 0 ? '+' : '' }}{{ pnl }}
              </div>
              <div class="game-stats">
                <span>Sessions: {{ gameSessionsCount[gameId] }}</span>
                <span>Bets: {{ gameBetsCount[gameId] }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div> -->
    <div class="dashboard-column transactions-column">
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
              <div class="transaction-category">{{ transaction.category }}</div>
              <div class="transaction-description">{{ transaction.description }}</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, computed } from 'vue';
import { useWalletStore } from '@/store/walletStore';
import api from '@/services/api';

const walletStore = useWalletStore();

const balance = computed(() => walletStore.balance);
const timestamp = computed(() => walletStore.timestamp);
const transactions = computed(() => walletStore.transactions);
const gamePnls = computed(() => walletStore.gamePnls);
const gameSessionsCount = computed(() => walletStore.gameSessionsCount);
const gameBetsCount = computed(() => walletStore.gameBetsCount);

onMounted(async () => {
  console.log('PlayerDash mounted! Fetching transactions...');
  try {
    const response = await api.get('/transactions');
    console.log('Transactions response:', response.data);
    walletStore.setTransactions(response.data.transactions);
  } catch (error) {
    console.error('Error fetching transactions:', error);
  }
  walletStore.initializeSSE();
});
</script>

<style scoped>
.player-dashboard-layout {
  display: flex;
  height: calc(100vh - 70px); /* Adjust header height if needed */
  gap: 20px;
  padding: 20px;
  box-sizing: border-box;
}

.dashboard-column {
  flex: 1 1 0;
  min-width: 0;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: transparent;
  overflow-y: auto;
  /* Optional: add a subtle border or shadow for separation */
}

.wallet-column,
.gamepnl-column,
.transactions-column {
  max-width: none;
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

.wallet-card span {
  font-size: 1.5em;
  font-weight: bold;
  color: #fff;
  display: flex;
  align-items: center;
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
  font-weight: bold;
  text-transform: capitalize;
  font-size: 0.95em;
}

.transaction-description {
  font-size: 0.85em;
  color: #666;
}

.game-pnl-section {
  margin-bottom: 30px;
}

.game-pnl-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 20px;
  margin-top: 15px;
}

.game-pnl-card {
  background-color: #343434;
  padding: 10px 12px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.08);
}

.game-pnl-card h3 {
  margin: 0 0 8px 0;
  color: #fff;
  font-size: 1em;
}

.pnl-value {
  font-size: 1.1em;
  font-weight: bold;
  margin-bottom: 6px;
}

.pnl-value.positive {
  color: #00ff00;
}

.pnl-value.negative {
  color: #ff0000;
}

.game-stats {
  font-size: 0.85em;
  color: #888;
}

.game-stats div {
  margin: 2px 0;
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
}
</style>
