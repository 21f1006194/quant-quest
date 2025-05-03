import { defineStore } from 'pinia';
import sseService from '@/services/sseService';

export const useWalletStore = defineStore('wallet', {
    state: () => ({
        balance: 0,
        timestamp: null,
        gamePnls: {},
        gameSessionsCount: {},
        gameBetsCount: {},
    }),

    actions: {
        initializeSSE() {
            // Subscribe to wallet and bet updates
            sseService.subscribe('wallet_update', this.handleWalletUpdate);
            sseService.subscribe('bet_update', this.betUpdate);
            sseService.connect();
        },
        betUpdate(data) {
            this.balance = data.balance;
            this.timestamp = data.timestamp;
            this.gamePnls[data.game_id] = data.pnl;
            this.gameSessionsCount[data.game_id] = data.session_count;
            this.gameBetsCount[data.game_id] = data.bet_count;
        },

        handleWalletUpdate(data) {
            this.balance = data.balance;
            this.timestamp = data.timestamp;
        },

        setWalletData(data) {
            this.balance = data.balance;
            this.timestamp = data.last_updated;
        },

        cleanup() {
            sseService.unsubscribe('wallet_update', this.handleWalletUpdate);
            sseService.unsubscribe('bet_update', this.betUpdate);
            sseService.cleanup();
        }
    }
});