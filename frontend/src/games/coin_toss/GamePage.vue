<template>
    <div class="game-page">
        <img src="@/games/coin_toss/assets/coin_toss_cover.jpg" alt="Coin Toss" class="header-banner" />
        <h1>Coin Toss Challenge</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>
                    Welcome to the Coin Toss Challenge! You'll be playing with a special coin that has its own unique characteristics. 
                    The same coin will be used throughout all of your sessions, giving you the opportunity to learn its patterns. 
                    Can you figure out which side it favors?
                </p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum rounds per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Payout: {{ gameData.config_data.payout }}x your bet</p>
                <p>Minimum bet: {{ gameData.config_data.min_bet_amount }}</p>
            </div>
            <div class="how-to-play">
                <h2>How to Play</h2>
                <ol>
                  <li>
                    <strong>Start a round (Toss the coin):</strong> <br />
                    Send an empty <code>POST</code> request to <code>/play/coin_toss</code> to toss the coin.
                  </li>
                  <li>
                    <strong>Make your Bet:</strong> <br />
                    Send a <code>PATCH</code> request to <code>/play/coin_toss</code> with your prediction choice and bet amount to place your bet.
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

            <div class="sct-tips">
                <h2>SCT Tips</h2>
                <p class="sct-note">Note: These tips are specific to the Coin Toss SCT and won't be available for other games.</p>
                <div class="tips-content">
                    <ul>
                        <li>Start with minimum bet ({{ gameData.config_data.min_bet_amount }} units) to understand the response structure</li>
                        <li>You have {{ gameData.max_sessions_per_user }} attempts with {{ gameData.config_data.payout }}x payout - use them wisely!</li>
                        <li>Use minimum bets to collect data and look for patterns in the coin's behavior</li>
                        <li>Once you have a strategy, implement it with larger bets</li>
                        <li>Remember: Maximum 3 API hits per second to avoid penalties</li>
                        <li>The same coin is used throughout all sessions - use this to your advantage!</li>
                        <li>Use the python template given below to get started</li>
                    </ul>
                </div>
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

.sct-tips {
    margin-top: 2rem;
    padding: 1rem;
    /* background-color: #f5f5f5; */
    border-radius: 8px;
}

.sct-note {
    color: #666;
    font-style: italic;
    margin-bottom: 1rem;
}

.tips-content {
    margin-top: 1rem;
}

.tips-content ul {
    list-style-type: none;
    padding-left: 1rem;
}

.tips-content li {
    margin-bottom: 0.5rem;
    position: relative;
    padding-left: 1.5rem;
}

.tips-content li:before {
    content: "•";
    color: #42b983;
    position: absolute;
    left: 0;
}
</style>
