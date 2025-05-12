<template>
    <div class="game-page">
        <img src="@/games/bayesian_ball/assets/bayesian_ball_cover.jpg" alt="Bayesian Ball" class="header-banner" />
        <h1>Bayesian Ball</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>
                  Step into the world of <strong>Bayesian Ball</strong>—where logic, deduction, and probability collide! Four mysterious bags, each with their own secret blend of Red, Green, and Blue balls, await your keen mind. Can you outsmart the odds and uncover the hidden patterns?
                </p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum rounds per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Payout: {{ gameData.config_data.payout }}</p>
            </div>
            <div class="how-to-play">
                <h2>How to Play</h2>
                <ol>
                  <li>
                    <strong>Start a round:</strong> <br />
                    Send a <code>POST</code> request to <code>/play/bayesian_ball</code> (include your API token as <code>X-API-Token</code> in the header). You'll receive 9 balls drawn (with replacement) from a secret bag—these are revealed to you. The 10th ball remains hidden!
                  </li>
                  <li>
                    <strong>Make your prediction:</strong> <br />
                    Send a <code>PATCH</code> request to <code>/play/bayesian_ball</code> with your guess for the <strong>10th ball's color</strong> and the <strong>bag</strong> you think was used.
                  </li>
                  <li>
                    <strong>See the results:</strong> <br />
                    The response will reveal the true 10th ball, the correct bag, and your payout info. You win if you nail <em>both</em> the color and the bag!
                  </li>
                </ol>
                <details>
                  <summary>Payload Example</summary>
                  <pre><code>// POST request (empty payload)
{}

// PATCH request
{
  "session_id": "string",
  "choice": "string", // First char: bag (A|B|C|D), Second char: color (R|G|B)
  "bet_amount": number
}</code></pre>
                </details>
                <details>
                  <summary>Response Example</summary>
                  <pre><code>// POST response
{
  "session_id": number,
  "balls": string[]  // Array of 9 balls (R|G|B)
}

// PATCH response
{
  "game_data": {
    "bag": string,    // A|B|C|D
    "balls": string[] // Array of 10 balls (R|G|B)
  },
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
                  Observe the clues, trust your logic, and let Bayesian reasoning guide you. Every round is a new puzzle—can you maximize your winnings and become the Bayesian Ball champion?
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
    template.value = await getGameTemplate('bayesian_ball')
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
