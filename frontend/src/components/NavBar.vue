<template>
<nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
        <a class="navbar-brand" href="#">QuantQuest</a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="#">Home</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#">About</a>
                </li>
                <li class="nav-item" v-if="!authStore.isAuthenticated">
                    <router-link class="nav-link" to="/login">Login</router-link>
                </li>
                <li class="nav-item" v-if="!authStore.isAuthenticated">
                    <router-link class="nav-link" to="/register">Register</router-link>
                </li>
                <li class="nav-item" v-if="authStore.isAuthenticated">
                    <button class="nav-link btn btn-link" @click="logout">Logout</button>
                </li>
            </ul>
        </div>
    </div>
</nav>



</template>

<script setup>
import { useAuthStore } from '../store/authStore';
import { useRouter } from 'vue-router';
import { computed, watchEffect } from 'vue';

const authStore = useAuthStore();
const router = useRouter();


const logout = () => {
    authStore.logout();
    router.push('/login');
};
watchEffect(() => {
  authStore.checkAuth(); // Ensure auth state is up-to-date
});
</script>

<style scoped>
.nav-link.btn {
  padding: 0;
  margin-left: 1rem;
}
</style>