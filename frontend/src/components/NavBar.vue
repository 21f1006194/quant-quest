<template>
  <nav class="navbar navbar-expand-lg">
    <div class="container-fluid">
      <router-link class="navbar-brand" to="/">
        <span class="brand-text">QuantQuest</span>
      </router-link>
      <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <!-- Anonymous User Navigation -->
        <ul v-if="!authStore.isAuthenticated" class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/about">About</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="https://iitmparadox.org/events/register/20" target="_blank" rel="noopener noreferrer">Register</a>
          </li>
        </ul>

        <!-- Admin Navigation -->
        <ul v-else-if="authStore.isAdmin" class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/admin">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/games">Games</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/players">Players</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/admin/whitelist">Whitelist</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
          </li>
          <li class="nav-item ms-auto d-flex align-items-center">
            <span class="nav-link username ms-3">Welcome, Admin</span>
          </li>
        </ul>

        <!-- Regular User Navigation -->
        <ul v-else class="navbar-nav">
          <li class="nav-item">
            <router-link class="nav-link" to="/player">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/games">Games</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/profile">Profile</router-link>
          </li>
          <li class="nav-item">
            <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
          </li>
          <li class="nav-item ms-auto d-flex align-items-center">
            <div class="wallet-balance">
              <img :src="CoinIcon" class="coin-icon" alt="coin" />
              <span>{{ walletStore.balance.toFixed(2) }}</span>
            </div>
            <div class="user-welcome ms-3">
              <template v-if="authStore.getAvatarUrl">
                <router-link to="/profile">
                  <img :src="authStore.getAvatarUrl" class="profile-pic" alt="Profile" />
                </router-link>
              </template>
              <template v-else>
                <span class="welcome-text">
                  {{ authStore.getFullName || authStore.user?.username }}
                </span>
              </template>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useAuthStore } from '@/store/authStore';
import { useWalletStore } from '@/store/walletStore';
import { useRouter } from 'vue-router';
import { computed, watchEffect } from 'vue';
import CoinIcon from '@/assets/coins-solid.svg';

const authStore = useAuthStore();
const walletStore = useWalletStore();
const router = useRouter();

const logout = () => {
    authStore.logout();
    router.push('/login');
};
watchEffect(() => {
  authStore.checkAuth();
});
</script>

<style scoped>
.navbar {
  background-color: var(--card-dark);
  padding: var(--spacing-md) var(--spacing-lg);
  box-shadow: var(--shadow-sm);
}

.navbar-brand {
  font-size: 1.5rem;
  font-weight: bold;
  color: var(--primary-color) !important;
  text-decoration: none;
}

.brand-text {
  background: linear-gradient(45deg, var(--primary-color), var(--secondary-color));
  -webkit-background-clip: text;
  background-clip: text;
  -webkit-text-fill-color: transparent;
  text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
}

.navbar-nav {
  width: 100%;
  gap: var(--spacing-sm);
}

.nav-link {
  color: var(--text-light) !important;
  padding: var(--spacing-xs) var(--spacing-sm) !important;
  border-radius: var(--border-radius-sm);
  transition: all var(--transition-normal);
}

.nav-link:hover {
  color: var(--primary-color) !important;
  background-color: rgba(100, 255, 218, 0.1);
}

.nav-link.router-link-active {
  color: var(--primary-color) !important;
  background-color: rgba(100, 255, 218, 0.1);
}

.username {
  color: var(--secondary-color) !important;
  font-style: italic;
}

.navbar-toggler {
  border-color: var(--primary-color);
}

.navbar-toggler-icon {
  background-image: url("data:image/svg+xml,%3csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 30 30'%3e%3cpath stroke='rgba(100, 255, 218, 1)' stroke-linecap='round' stroke-miterlimit='10' stroke-width='2' d='M4 7h22M4 15h22M4 23h22'/%3e%3c/svg%3e");
}

.wallet-balance {
  display: flex;
  align-items: center;
  gap: 8px;
  color: #00ff00;
  font-weight: bold;
}

.coin-icon {
  width: 1.2em;
  height: 1.2em;
  filter: invert(1) sepia(1) saturate(10000%) hue-rotate(80deg);
}

.user-welcome {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.profile-pic {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  object-fit: cover;
  border: 2px solid var(--primary-color);
}

.welcome-text {
  color: var(--secondary-color);
  font-style: italic;
}

@media (max-width: 768px) {
  .navbar {
    padding: var(--spacing-xs) var(--spacing-sm);
  }
  
  .navbar-nav {
    padding: var(--spacing-sm) 0;
  }
  
  .nav-link {
    padding: var(--spacing-xs) !important;
  }
  
  .wallet-balance {
    margin: 8px 0;
    justify-content: center;
  }
  
  .nav-item.ms-auto {
    flex-direction: column;
    align-items: center !important;
  }
  
  .user-welcome {
    margin-top: 8px;
    margin-left: 0 !important;
  }
  
  .profile-pic {
    width: 28px;
    height: 28px;
  }
}
</style>