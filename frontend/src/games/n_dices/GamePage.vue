<template>
    <div class="game-page">
        <img src="@/games/n_dices/assets/n_dices_cover.jpg" alt="N Dice" class="header-banner" />
        <h1>N Dices</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
            <p>
                N number of dices are rolled. The sum of the dice is calculated. If the sum is equal to the player's bet, the player wins. If the sum is not equal to the player's bet, the player loses.
            </p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum bets per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Payout: {{ gameData.config_data.payout }}</p>
                <p>Minimum bet amount: {{ gameData.config_data.min_bet_amount  }}</p>
            </div>
            
                <div class="how-to-play">
                    <h2>How to Play</h2>
                    <p>The game is played in two steps:</p>
                    <ol>
                        <li>
                            <p>First, send a POST request to the endpoint <code>/play/n_dice</code> to get the number of dice for the round. Include your API token in the header as <code>X-API-Token</code>.</p>
                            <details>
                                <summary>Response</summary>
                                <pre><code>{
    "session_id": number,
    "n": number
}</code></pre>
                                <ul>
                                    <li><code>session_id</code>: The session identifier for this round.</li>
                                    <li><code>n</code>: The number of dice for this round.</li>
                                </ul>
                            </details>
                        </li>
                        <li>
                            <p>Then, place your bet by sending another POST request to <code>/play/n_dice</code> with your guess for the sum.</p>
                            <details>
                                <summary>Payload</summary>
                                <pre><code>{
    "session_id": number, // from the first step
    "choice": number between n and 6n,
    "bet_amount": number
}</code></pre>
                                <ul>
                                    <li><code>choice</code>: The number you bet on, between n and 6n (where n is the number of dice).</li>
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
    },
    "current_balance": number
}</code></pre>
                                <ul>
                                    <li><code>dice_sum</code>: The total sum of the dice rolls.</li>
                                    <li><code>result</code>: Indicates if you "win" or "loss".</li>
                                    <li><code>payout</code>: The payout amount if you win (20x your bet).</li>
                                    <li><code>current_balance</code>: Your updated balance after the bet.</li>
                                </ul>
                            </details>
                        </li>
                    </ol>
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
    template.value = await getGameTemplate('n_dices')
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