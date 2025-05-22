import { defineStore } from 'pinia';
import { ref } from 'vue';
import sseService from '@/services/sseService';
import { useNotificationStore } from '@/store/notificationStore';

export const useWalletStore = defineStore('wallet', () => {
    const balance = ref(0);
    const timestamp = ref(null);
    const transactions = ref([]);

    function initializeSSE() {
        sseService.subscribe('wallet_update', handleWalletUpdate);
        sseService.subscribe('transaction_update', transactionUpdate);
        sseService.connect();
    }

    function transactionUpdate(data) {
        transactions.value.push(data.transaction);
        balance.value = parseFloat(data.balance.toFixed(2));
        timestamp.value = data.timestamp;

        const notification = useNotificationStore();
        const isBonus = data.transaction.category === 'bonus';
        const color = isBonus ? 'green' : 'red';
        const sign = isBonus ? '+' : '-';
        const message = `${sign}${Math.abs(data.transaction.amount)} — ${data.transaction.description}`;
        notification.show(message, color);
    }

    function handleWalletUpdate(data) {
        balance.value = parseFloat(data.balance.toFixed(2));
        timestamp.value = data.timestamp;
    }

    function setWalletData(data) {
        balance.value = parseFloat(data.balance.toFixed(2));
        timestamp.value = data.last_updated;
    }

    function cleanup() {
        sseService.unsubscribe('wallet_update', handleWalletUpdate);
        sseService.unsubscribe('transaction_update', transactionUpdate);
        sseService.cleanup();
    }

    function setTransactions(newTransactions) {
        transactions.value = newTransactions;
    }

    return {
        balance,
        timestamp,
        transactions,
        initializeSSE,
        transactionUpdate,
        handleWalletUpdate,
        setWalletData,
        cleanup,
        setTransactions
    };
});