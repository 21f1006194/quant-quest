import { defineStore } from 'pinia';
import { ref } from 'vue';
import sseService from '@/services/sseService';
import { useWalletStore } from '@/store/walletStore';

export const useGameStore = defineStore('game', () => {
    const games = ref([]);
    const gamePnls = ref(new Map());
    const gameSessionsCount = ref(new Map());
    const gameBetsCount = ref(new Map());

    function initializeGames(gamesData) {
        games.value = gamesData;
        gamesData.forEach(game => {
            gamePnls.value.set(game.id, parseFloat(game.pnl.toFixed(2)));
            gameSessionsCount.value.set(game.id, game.session_count);
            gameBetsCount.value.set(game.id, game.bet_count);
        });
    }

    function handleBetUpdate(data) {
        gamePnls.value.set(data.game_id, parseFloat(data.pnl.toFixed(2)));
        gameSessionsCount.value.set(data.game_id, data.session_count);
        gameBetsCount.value.set(data.game_id, data.bet_count);

        // Update wallet balance as well
        const walletStore = useWalletStore();
        walletStore.handleWalletUpdate({
            balance: parseFloat(data.balance.toFixed(2)),
            timestamp: data.timestamp
        });
    }

    function initializeSSE() {
        sseService.subscribe('bet_update', handleBetUpdate);
        sseService.connect();
    }

    function cleanup() {
        sseService.unsubscribe('bet_update', handleBetUpdate);
        sseService.cleanup();
    }

    return {
        games,
        gamePnls,
        gameSessionsCount,
        gameBetsCount,
        initializeGames,
        handleBetUpdate,
        initializeSSE,
        cleanup
    };
});