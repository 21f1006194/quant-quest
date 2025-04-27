<template>
  <div class="app-container">
    <nav-bar/>
    <router-view/>
  </div>
</template>

<script setup>
import NavBar from './components/NavBar.vue';
import { RouterView } from 'vue-router';
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