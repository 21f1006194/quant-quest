<template>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">QuantQuest</a>
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
                    <router-link class="nav-link" to="/register">Register</router-link>
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
                    <a class="nav-link" href="#" @click.prevent="logout">Logout</a>
                </li>
                <li class="nav-item ms-auto">
                    <span class="nav-link">Welcome, {{ authStore.user?.username }}</span>
                </li>
            </ul>

            <!-- Regular User Navigation -->
            <ul v-else class="navbar-nav">
                <li class="nav-item">
                    <router-link class="nav-link" to="/">Home</router-link>
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
                <li class="nav-item ms-auto">
                    <span class="nav-link">Welcome, {{ authStore.user?.username }}</span>
                </li>
            </ul>
        </div>
    </div>
</nav>
</template>

<script setup>
import { useAuthStore } from '../store/authStore';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const router = useRouter();

const logout = () => {
    authStore.logout();
    router.push('/login');
};
</script>

<style scoped>
.navbar-nav {
    width: 100%;
}

.nav-link {
    cursor: pointer;
}

.ms-auto {
    margin-left: auto !important;
}
</style>