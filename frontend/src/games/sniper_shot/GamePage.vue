<template>
    <div class="game-page">
        <img src="@/games/sniper_shot/assets/sniper_banner.png" alt="Sniper Shot" class="header-banner" />
        <h1>Sniper Shot</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>
                    Step into the boots of a regiment commander in <strong>Sniper Shot</strong>—a high-stakes test of intuition, leadership, and probability. You command a squad of 27 elite snipers, each taking a shot at their designated target under your watch.
                </p>
                <p>
                    Your mission isn't to pull the trigger, but to anticipate performance — <strong>place your wager on how many snipers will hit their mark</strong>. Each sniper fires independently, and success is never guaranteed. Will your judgment prove sharp under pressure, or will uncertainty cloud your call?
                </p>
                <p>
                    Your goal: <strong>Predict the total number of successful hits</strong> across all 27 snipers. Think tactically, weigh the odds, and trust your instincts — the outcome of this operation depends on your ability to read the battlefield from afar.
                </p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum bets per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Payout: {{ gameData.config_data.payout }}</p>
            </div>
            
            <div class="how-to-play">
                <h2>How to Play</h2>
                <p>To play the game, send a POST request to the endpoint <code>/play/sniper_shot</code>. Include your API token in the header as <code>X-API-Token</code>.</p>
                <details>
                    <summary>Payload</summary>
                    <pre><code>{
    "choice": number between 0 and 27,
    "bet_amount": number
}</code></pre>
                    <ul>
                        <li><code>choice</code>: The number you choose to bet on.</li>
                        <li><code>bet_amount</code>: The amount you wish to bet.</li>
                    </ul>
                </details>
                <details>
                    <summary>Response</summary>
                    <pre><code>{
    "result": {
        // Game specific result data
    },
    "current_balance": number
}</code></pre>
                    <ul>
                        <li><code>result</code>: Contains the game result data.</li>
                        <li><code>current_balance</code>: Your updated wallet balance after the bet.</li>
                    </ul>
                </details>
                <details>
                    <summary>Error Response</summary>
                    <pre><code>{
    "error": string
}</code></pre>
                    <p>Returns HTTP 400 status code with error message if the request is invalid.</p>
                </details>
            </div>
            
            <details>
                <summary>Python Template</summary>
                <PythonTemplate v-if="template" :code="template" :game_name="gameData.name" />
            </details>
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
    template.value = await getGameTemplate('sniper_shot')
})
</script>

<style scoped>
.game-info {
    max-width: 800px;
    margin: 0 auto;
    padding: 1rem;
}

.header-banner {
    width: 100%;
    height: auto;
    max-height: 300px;
    object-fit: cover;
    margin-bottom: 1rem;
}
</style>

