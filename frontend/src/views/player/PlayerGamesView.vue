<template>
    <div class="games-container">
        <h1>Games</h1>
        <div class="games-grid">
            <GameCard
                v-for="game in games"
                :key="game.id"
                :game-name="game.name"
                :max-sessions="game.max_sessions_per_user"
                :sessions-used="walletStore.gameSessionsCount[game.id]"
                :max-bets="game.max_bets_per_session"
                :difficulty="game.difficulty"
                :tags="game.tags"
                :pnl="walletStore.gamePnls[game.id]"
            />
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { useWalletStore } from '@/store/walletStore';
import GameCard from '@/components/game/GameCard.vue';

const games = ref([]);
const loading = ref(false);
const error = ref(null);
const walletStore = useWalletStore();

const fetchGames = async () => {
    loading.value = true;
    const response = await api.get('/games');
    if (response.status === 200) {
        games.value = response.data.games;
        // Initialize game PNLs in wallet store
        games.value.forEach(game => {
            walletStore.gamePnls[game.id] = game.pnl;
            walletStore.gameSessionsCount[game.id] = game.session_count;
            walletStore.gameBetsCount[game.id] = game.bet_count;
        });
    } else {
        games.value = [];
        error.value = response.data.message;
    }
    loading.value = false;
};

onMounted(() => {
    fetchGames();
});
</script>

<style scoped>
.games-container {
    padding: 2rem;
    width: 100%;
    display: flex;
    flex-direction: column;
    align-items: center;
}

h1 {
    text-align: center;
    margin-bottom: 2rem;
    color: #ffffff;
    font-size: 2rem;
    font-weight: 600;
}

.games-grid {
    display: flex;
    flex-direction: column;
    gap: 1rem;
    align-items: center;
    width: 90%;
}
</style>