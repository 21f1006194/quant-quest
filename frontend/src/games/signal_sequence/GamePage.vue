<template>
    <div class="game-page">
        <img src="@/games/signal_sequence/assets/signal_sequence_cover.jpg" alt="Signal Sequence" class="header-banner" />
        <h1>Signal Sequence</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>
                    Welcome to <strong>Signal Sequence</strong>—an exciting puzzle game where you decode a hidden sequence of colored signal lights! The game features five colors: Red, Blue, Green, Yellow, and Purple, each with a subtly biased probability distribution.
                </p>
                <div class="mb-8">
                    The game mechanics are simple yet challenging:
                    <ul>
                        <li>Signals turn on one by one in a sequence</li>
                        <li>You must predict each color in the correct order</li>
                        <li>Each correct guess builds your streak</li>
                        <li>A single mistake ends the round</li>
                        <li>You can make up to four predictions in each game session</li>
                    </ul>
                </div>
                
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum rounds per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Bets per round: 4</p>
                <p>Minimum bet amount: 30</p>
                <p>Available colors: Red, Blue, Green, Yellow, Purple</p>
            </div>
            <div class="how-to-play">
                <h2>How to Play</h2>
                <ol>
                  <li>
                    <strong>Start a game:</strong> <br />
                    Send a <code>POST</code> request to <code>/play/signal_sequence</code> (include your API token as <code>X-API-Token</code> in the header). You'll receive a session ID to track your game.
                  </li>
                  <li>
                    <strong>Make your prediction:</strong> <br />
                    Send a <code>PATCH</code> request to <code>/play/signal_sequence</code> with your color choice, bet amount, and the session ID.
                  </li>
                  <li>
                    <strong>See the results:</strong> <br />
                    The response will reveal if your prediction was correct and show your current streak. Continue making predictions until you make a mistake or reach the maximum of four predictions.
                  </li>
                </ol>
                <details>
                  <summary>Payload Example</summary>
                  <pre><code>// POST request (empty payload)
{}

// PATCH request
{
  "session_id": "string",
  "choice": "string",    // Color choice ("Red", "Blue", "Green", "Yellow", or "Purple")
  "bet_amount": number
}</code></pre>
                </details>
                <details>
                  <summary>Response Example</summary>
                  <pre><code>// POST response
{
  "session_id": number,
  "message": "Game started, now place your bet."
}

// PATCH response
{
  "session_id": number,
  "payout": number,
  "sequence": string[],
  "streak": number,
  "current_balance": number
}</code></pre>
                </details>
                <details>
                  <summary>Error Response</summary>
                  <pre><code>{
  "error": string
}</code></pre>
                  <p>Returns HTTP 400 status code with error message if the request is invalid.</p>
                </details>
            </div>
            <div class="goal">
                <h2>Your Mission</h2>
                <p>
                  Use your statistical reasoning and pattern recognition skills to detect the hidden color distribution. Each game is a new opportunity to test your ability to identify patterns and make informed predictions. Can you become the Signal Sequence master?
                </p>
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
import { getGameTemplate } from '@/services/gameService'
import { ref, onMounted } from 'vue'
import PythonTemplate from '@/components/game/PythonTemplate.vue'

const route = useRoute()
const gameData = route.meta.gameData
const template = ref(null)

onMounted(async () => {
    template.value = await getGameTemplate('signal_sequence')
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
