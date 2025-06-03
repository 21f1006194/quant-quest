<template>
    <div v-if="show" class="modal-overlay" @click="close">
        <div class="modal-content" @click.stop>
            <div class="modal-header">
                <h2>Player Details</h2>
                <button class="close-btn" @click="close">
                    <i class="bi bi-x"></i>
                </button>
            </div>
            
            <div class="player-profile">
                <div class="profile-header">
                    <img :src="playerData.avatar_url" alt="Profile Picture" class="profile-picture">
                    <div class="profile-info">
                        <h3>{{ playerData.full_name }}</h3>
                        <p class="user-id">_id: {{ playerData.id }}</p>
                        <p class="username">user: {{ playerData.username }}</p>
                        <p class="username"> email: {{ playerData.email }}</p>
                    </div>
                </div>

                <div class="wallet-section">
                    <div class="wallet-info">
                        <h4>Wallet Balance</h4>
                        <p class="balance">${{ playerData.wallet_balance }}</p>
                        <p class="last-updated">Last Updated: {{ formatDate(playerData.wallet_last_updated) }}</p>
                    </div>
                    <div class="total-pnl">
                        <h4>Total PnL</h4>
                        <p :class="['pnl-value', playerData.total_pnl >= 0 ? 'positive' : 'negative']">
                            ${{ playerData.total_pnl }}
                        </p>
                    </div>
                </div>

                <div class="games-section">
                    <h4>Game Performance</h4>
                    <div class="games-list">
                        <div v-for="game in playerData.games.filter(g => g.pnl !== 0)" :key="game.game_id" class="game-item">
                            <span class="game-name">{{ game.game_name }}</span>
                            <span :class="['game-pnl', game.pnl >= 0 ? 'positive' : 'negative']">
                                ${{ game.pnl }}
                            </span>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
    show: Boolean,
    playerData: Object
});

const emit = defineEmits(['close']);

const close = () => {
    emit('close');
};

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
};
</script>

<style scoped>
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background-color: rgba(0, 0, 0, 0.5);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
}

.modal-content {
    background: white;
    border-radius: 8px;
    padding: 1.5rem;
    width: 90%;
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
}

.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.modal-header h2 {
    margin: 0;
    color: #2c3e50;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #666;
}

.profile-header {
    display: flex;
    gap: 1.5rem;
    margin-bottom: 2rem;
}

.profile-picture {
    width: 100px;
    height: 100px;
    border-radius: 50%;
    object-fit: cover;
}

.profile-info h3 {
    margin: 0 0 0.5rem 0;
    color: #2c3e50;
}

.username, .user-id {
    margin: 0.25rem 0;
    color: #666;
}

.wallet-section {
    display: flex;
    justify-content: space-between;
    margin-bottom: 2rem;
    padding: 1rem;
    background: #f8f9fa;
    border-radius: 8px;
}

.wallet-info, .total-pnl {
    text-align: center;
}

.wallet-info h4, .total-pnl h4 {
    margin: 0 0 0.5rem 0;
    color: #2c3e50;
}

.balance {
    font-size: 1.5rem;
    font-weight: bold;
    color: #2c3e50;
    margin: 0;
}

.last-updated {
    font-size: 0.8rem;
    color: #666;
    margin: 0.5rem 0 0 0;
}

.pnl-value {
    font-size: 1.5rem;
    font-weight: bold;
    margin: 0;
}

.positive {
    color: #4CAF50;
}

.negative {
    color: #f44336;
}

.games-section {
    margin-top: 1.5rem;
}

.games-section h4 {
    margin: 0 0 1rem 0;
    color: #2c3e50;
}

.games-list {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.game-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0.75rem;
    background: #f8f9fa;
    border-radius: 6px;
}

.game-name {
    font-weight: 500;
    color: #2c3e50;
}

.game-pnl {
    font-weight: 500;
}
</style>
