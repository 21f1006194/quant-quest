<template>
  <div class="game-wrapper">
    <router-view></router-view>
  </div>
</template>

<script setup>
defineOptions({
  name: 'GameWrapper'
})
</script>


<style scoped>

.game-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  width: 100%;
}

.game-page {
  width: 80%;
  margin: 0 auto;
}
</style>