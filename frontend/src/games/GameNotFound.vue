<template>
  <div class="game-not-found">
    <div class="card">
      <h1>Game Not Found</h1>
      <p class="text-secondary">The game you're looking for couldn't be found.</p>
      
      <div class="suggestions">
        <h3>What you can do:</h3>
        <ul>
          <li>Check if the game URL is correct</li>
          <li>Verify if the game is still available</li>
          <li>Contact support if you believe this is an error</li>
        </ul>
      </div>

      <router-link :to="authStore.isUser ? '/player' : '/'" class="btn btn-primary">
        Return to {{ authStore.isUser ? 'Player Dashboard' : 'Homepage' }}
      </router-link>
    </div>
  </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { useAuthStore } from '../store/authStore'

const route = useRoute()
const authStore = useAuthStore()
</script>

<style scoped>
.game-not-found {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: var(--spacing-lg);
}

.card {
  max-width: 600px;
  width: 100%;
  text-align: center;
}

h1 {
  margin-bottom: var(--spacing-md);
}

.text-secondary {
  margin-bottom: var(--spacing-lg);
}

.suggestions {
  text-align: left;
  margin: var(--spacing-xl) 0;
  padding: var(--spacing-lg);
  background-color: var(--background-dark);
  border-radius: var(--border-radius-md);
}

.suggestions h3 {
  margin-bottom: var(--spacing-md);
  color: var(--primary-color);
}

.suggestions ul {
  list-style-type: none;
  padding-left: 0;
}

.suggestions li {
  margin-bottom: var(--spacing-sm);
  padding-left: var(--spacing-lg);
  position: relative;
  color: var(--text-light);
}

.suggestions li::before {
  content: "•";
  color: var(--primary-color);
  position: absolute;
  left: 0;
}

.btn {
  margin-top: var(--spacing-xl);
}
</style>