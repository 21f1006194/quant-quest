<template>
    <div class="game-page">
        <img src="@/games/coin_toss/assets/coin_toss_cover.jpg" alt="Coin Toss" class="header-banner" />
        <h1>Coin Toss Challenge</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>
                    Welcome to the Coin Toss Challenge! You'll be playing with a special coin that has its own unique characteristics. 
                    The same coin will be used throughout your session, giving you the opportunity to learn its patterns. 
                    Can you figure out which side it favors?
                </p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum rounds per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Payout: {{ gameData.config_data.payout }}x your bet</p>
                <p>Minimum bet: 10</p>
            </div>
            <div class="how-to-play">
                <h2>How to Play</h2>
                <ol>
                  <li>
                    <strong>Start a round:</strong> <br />
                    Send a <code>POST</code> request to <code>/play/coin_toss</code> with your API token in the header.
                  </li>
                  <li>
                    <strong>Make your Bet:</strong> <br />
                    Send a <code>PATCH</code> request to <code>/play/coin_toss</code> with your prediction and bet amount.
                  </li>
                  <li>
                    <strong>See the results:</strong> <br />
                    The response will show you the outcome and your winnings.
                  </li>
                </ol>
                <details>
                  <summary>Request Details</summary>
                  <pre><code>// POST request (empty payload)
{}

// PATCH request
{
  "session_id": "number",    // Session ID from POST response
  "choice": "string",       // "H" for Heads or "T" for Tails
  "bet_amount": number      // Minimum bet: 10 units
}</code></pre>
                </details>
                <details>
                  <summary>Response Details</summary>
                  <pre><code>// POST response
{
  "session_id": number,
  "message": "Toss completed, now place your bet."
}

// PATCH response
{
  "toss_result": "string",  // "H" or "T"
  "payout": number,         // Your winnings (if any)
  "current_balance": number // Your updated balance
}</code></pre>
                </details>
                <details>
                  <summary>Error Response</summary>
                  <pre><code>{
  "error": "string"  // Error message
}</code></pre>
                  <p>Returns HTTP 400 status code with error message if the request is invalid.</p>
                </details>
            </div>
            <div class="goal">
                <h2>Your Mission</h2>
                <p>
                  Watch the patterns, trust your instincts, and make your predictions. 
                  Each toss is a chance to learn more about this unique coin. 
                  Can you master its behavior and maximize your winnings?
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
    template.value = await getGameTemplate('coin_toss')
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
