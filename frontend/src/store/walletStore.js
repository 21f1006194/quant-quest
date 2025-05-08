import { defineStore } from 'pinia';
import sseService from '@/services/sseService';
import { useNotificationStore } from '@/store/notificationStore';

export const useWalletStore = defineStore('wallet', {
    state: () => ({
        balance: 0,
        timestamp: null,
        gamePnls: {},
        gameSessionsCount: {},
        gameBetsCount: {},
        transactions: [],
    }),

    actions: {
        initializeSSE() {
            // Subscribe to wallet and bet updates
            sseService.subscribe('wallet_update', this.handleWalletUpdate);
            sseService.subscribe('bet_update', this.betUpdate);
            sseService.subscribe('transaction_update', this.transactionUpdate);
            sseService.connect();
        },

        transactionUpdate(data) {
            this.transactions.push(data.transaction);
            this.balance = data.balance;
            this.timestamp = data.timestamp;
            const notification = useNotificationStore();
            const isBonus = data.transaction.category === 'bonus';
            const color = isBonus ? 'green' : 'red';
            const sign = isBonus ? '+' : '-';
            const message = `${sign}${Math.abs(data.transaction.amount)} — ${data.transaction.description}`;
            console.log(message, color);
            notification.show(message, color);
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
        },

        setTransactions(transactions) {
            this.transactions = transactions;
        }
    }
});