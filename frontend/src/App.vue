<template>
  <div class="app-container">
    <Notification />
    <nav-bar/>
    <router-view/>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue';
import { RouterView } from 'vue-router';
import { onMounted, onUnmounted, watch } from 'vue';
import { useWalletStore } from '@/store/walletStore';
import { useAuthStore } from '@/store/authStore';
import api from '@/services/api';
import Notification from './components/Notification.vue';

const walletStore = useWalletStore();
const authStore = useAuthStore();

const initializeWallet = async () => {
  if (!authStore.isAuthenticated) {
    return;
  }

  try {
    const response = await api.get('/wallet');
    if (response.status === 200) {
      walletStore.setWalletData(response.data.wallet);
      walletStore.initializeSSE();
    }
  } catch (error) {
    console.error('Failed to fetch initial wallet data:', error);
  }
};

// Watch for authentication state changes
watch(
  () => authStore.isAuthenticated,
  (isAuthenticated) => {
    if (isAuthenticated) {
      initializeWallet();
    } else {
      walletStore.cleanup();
    }
  }
);

onMounted(() => {
  // Initialize wallet if already authenticated
  if (authStore.isAuthenticated) {
    initializeWallet();
  }
});

onUnmounted(() => {
  if (authStore.isAuthenticated) {
    walletStore.cleanup();
  }
});
</script>

<style>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.router-link-active {
  color: var(--primary-color) !important;
  font-weight: bold;
}
</style>