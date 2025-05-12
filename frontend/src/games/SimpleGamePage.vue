<template>
    <div class="game-page">
        <div v-if="gameData" class="game-info">
            <div class="description markdown-body" v-html="renderedDescription"></div>
            <div class="config">
                <h3>Game Configuration</h3>
                <div v-for="(value, key) in gameData.config_data" :key="key">
                    <p>{{ key }}: {{ value }}</p>
                </div>
                <p>Max Sessions per User: {{ gameData.max_sessions_per_user }}</p>
                <p>Max Bets per Session: {{ gameData.max_bets_per_session }}</p>
            </div>
            <PythonTemplate v-if="template" :code="template" :game_name="gameData.name" />
        </div>
    </div>
</template>

<script setup>
import { useRoute } from 'vue-router'
import { marked } from 'marked'
import { getGameTemplate } from '@/services/gameService'
import { ref, onMounted, computed } from 'vue'
import PythonTemplate from '@/components/game/PythonTemplate.vue'

const route = useRoute()
const gameData = route.meta.gameData
const template = ref(null)

const renderedDescription = computed(() => {
    return marked(gameData?.description || '')
})

onMounted(async () => {
    template.value = await getGameTemplate(gameData.name)
})
</script>

<style scoped>

.game-info {
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
}

</style>