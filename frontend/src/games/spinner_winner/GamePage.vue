<template>
    <div class="game-page">
        <img src="@/games/spinner_winner/assets/spinner_winner_cover.jpg" alt="Spinner Winner" class="header-banner" />
        <h1>Spinner Winner</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>
                  Welcome to <strong>Spinner Winner</strong>—a thrilling game of chance and strategy! Watch as the wheel spins, revealing a sequence of colors. Your challenge is to predict the next color that will appear. Will you trust your intuition or analyze the patterns? Place your bets and let the wheel decide your fate!
                </p>
                <p>
                  Some colors are big and common, others small but highly rewarding.
                  Choose wisely. The smartest bet isn't always the safest.
                </p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum rounds per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Minimum bet amount: {{ gameData.config_data.min_bet_amount }}</p>
                <p>Payout: Depends on the color you bet on</p>
            </div>
            <div class="how-to-play">
                <h2>How to Play</h2>
                <ol>
                  <li>
                    <strong>Start a round:</strong> <br />
                    Send a <code>POST</code> request to <code>/play/spinner_winner</code> You'll receive the current state of the wheel (colors, their sizes and payouts)and a session ID to track your game.
                  </li>
                  <li>
                    <strong>Place your bet:</strong> <br />
                    Send a <code>PATCH</code> request to <code>/play/spinner_winner</code> with your prediction for the color you want to bet on and the amount you want to bet.
                  </li>
                  <li>
                    <strong>See the results:</strong> <br />
                    The response will reveal the wheel's final state, your payout, and updated balance. Win big by correctly predicting the right color!
                  </li>
                </ol>
                <details>
                  <summary>Payload Example</summary>
                  <pre><code>// POST request (empty payload)
{}

// PATCH request
{
  "session_id": "string",
  "choice": "string", // Color to bet on (e.g., "Red", "Green", "Blue")
  "bet_amount": number
}</code></pre>
                </details>
                <details>
                  <summary>Response Example</summary>
                  <pre><code>// POST response
{
  "session_id": number,
  "wheel": [
    {
      "color": "string",
      "start_angle": number,
      "end_angle": number,
      "payout": number
    },
    {
      "color": "string",
      "start_angle": number,
      "end_angle": number,
      "payout": number
    }
    ...
  ]

// PATCH response
{
  "game_data": {
    "wheel": [{},{},{}] // wheel state
  },
  "spin_angle": number, //the angle on which the wheel stopped
  "payout": number,
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
                  Watch the wheel spin, analyze the patterns, and make your predictions. Every spin is a new opportunity to win big. Can you master the art of prediction and become the ultimate Spinner Winner?
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
    template.value = await getGameTemplate('spinner_winner')
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
