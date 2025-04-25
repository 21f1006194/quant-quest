<template>
    <div class="game-not-active">
        <h2>Game Not Active</h2>
        <p>This game is currently not active. Please contact the administrator for more information.</p>
        <router-link to="/player" class="back-link">Back to Dashboard</router-link>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router'

const route = useRoute()
</script>

<style scoped>
.game-not-active {
    text-align: center;
    padding: 2rem;
    background-color: #fff3cd;
    border: 1px solid #ffeeba;
    border-radius: 4px;
    color: #856404;
    max-width: 600px;
    margin: 2rem auto;
}

h2 {
    margin-bottom: 1rem;
    color: #856404;
}

.back-link {
    display: inline-block;
    margin-top: 1rem;
    color: #856404;
    text-decoration: underline;
}

.back-link:hover {
    color: #6d4c00;
}
</style> 