<template>
    <div class="game-page">
        <img src="@/games/ten_dice/assets/green_dice.jpg" alt="Green Dice" class="header-banner" />
        <h1>Ten Dice</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>Player bets on a number between 10 and 60. The dice is rolled 10 times and the sum of the dice is calculated. If the sum is equal to the player's bet, the player wins. If the sum is not equal to the player's bet, the player loses.</p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum bets per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Payout: {{ gameData.config_data.payout }}</p>
            </div>
            
                <div class="how-to-play">
                    <h2>How to Play</h2>
                    <p>To play the game, send a POST request to the endpoint <code>/play/ten_dice</code>. Include your API token in the header as <code>X-API-Token</code>.</p>
                    <details>
                        <summary>Payload</summary>
                        <pre><code>{
    "choice": number between 10 and 60,
    "bet_amount": number
}</code></pre>
                        <ul>
                            <li><code>choice</code>: The number you bet on, between 10 and 60.</li>
                            <li><code>bet_amount</code>: The amount you wish to bet.</li>
                        </ul>
                    </details>
                    <details>
                        <summary>Response</summary>
                        <pre><code>{
    "result": {
        "dice_sum": number,
        "result": string,
        "payout": number
    }
}</code></pre>
                        <ul>
                            <li><code>dice_sum</code>: The total sum of the dice rolls.</li>
                            <li><code>result</code>: Indicates if you "win" or "lose".</li>
                            <li><code>payout</code>: The payout amount if you win.</li>
                        </ul>
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
    template.value = await getGameTemplate('ten_dice')
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