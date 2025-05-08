<template>
    <div>
        <h1>Games</h1>
    <div class="games-table games-table-container">
        <table>
            <thead>
                <tr>
                    <th>Game Name</th>
                    <th>Plays Remaining</th>
                    <th>Bets/Play</th>
                    <th>Difficulty</th>
                    <th>Tags</th>
                    <th>PnL</th>
                    <th>Play Game</th>
                </tr>
            </thead>
            <tbody>
                <tr v-for="game in games" :key="game.id">
                    <td>{{ game.name.replace(/_/g, ' ').split(' ').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ') }}</td>
                    <td>{{ game.max_sessions_per_user - walletStore.gameSessionsCount[game.id] }} / {{ game.max_sessions_per_user }}</td>
                    <td>{{ game.max_bets_per_session }}</td>
                    <td>{{ game.difficulty }}</td>
                    <td class="tags-cell">
                        <div class="tags-container">
                            <span v-for="tag in game.tags.split(',').map(tag => tag.trim())" :key="tag">
                                <span class="tag-pill">{{ tag }}</span>
                            </span>
                        </div>
                    </td>
                    <td>
                        <span v-if="walletStore.gamePnls[game.id] > 0" class="positive-pnl">{{ walletStore.gamePnls[game.id] }}</span>
                        <span v-else class="negative-pnl">{{ walletStore.gamePnls[game.id] }}</span>
                    </td>
                    <td>
                        <router-link :to="`/game/${game.name}`">
                            <i class="bi bi-play-btn-fill" style="font-size: 2em;"></i>
                        </router-link>
                    </td>
                </tr>
            </tbody>
        </table>
    </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { useWalletStore } from '@/store/walletStore';

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
h1 {
    text-align: center;
    margin-top: 20px;
}
.games-table-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    border-collapse: collapse;
    margin-top: 20px;
}

.games-table th, .games-table td {
    border: 1px solid #ddd;
    padding: 8px;
    text-align: left;
    vertical-align: middle;
}


.games-table th {
    background-color: #343434;
}

.games-table tr:nth-child(even) {
    background-color: #343434;
}

.games-table tr:hover {
    background-color: #585858;
}   

.tags-cell {
    min-width: 150px;
    max-width: 200px;
}

.tags-container {
    display: flex;
    flex-wrap: wrap;
    gap: 5px;
    align-items: center;
    justify-content: flex-start;
    min-height: 100%;
}

.tag-pill {
    background-color: #343434;
    color: #fff;
    padding: 5px 10px;
    border-radius: 5px;
    display: inline-block;
    white-space: nowrap;
}

.positive-pnl {
    color: #00ff00;
}

.negative-pnl {
    color: #ff0000;
}

td {
    height: 100%;
    display: table-cell;
    vertical-align: middle;
}

td:has(.tag-pill) {
    min-width: 200px;
}

</style>