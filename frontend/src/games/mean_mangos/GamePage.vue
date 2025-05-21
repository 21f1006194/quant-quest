<template>
    <div class="game-page">
        <img src="@/games/mean_mangos/assets/mean_mangos_cover.jpg" alt="Mean Mangos" class="header-banner" />
        <h1>Mean Mangos</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>
                  Welcome to <strong>Mean Mangos</strong>! In a bustling market town, mango prices have been swinging wildly for weeks. You've tracked the price for 50 days—now it's your chance to make a move. Will you buy or sell? Ten days later, you'll discover if your instincts paid off!
                </p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum rounds per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Minimum trade quantity: {{ gameData.config_data.min_qty }}</p>
            </div>
            <div class="how-to-play">
                <h2>How to Play</h2>
                <ol>
                  <li>
                    <strong>Start a round:</strong> <br />
                    Send a <code>POST</code> request to <code>/play/mean-mangos</code> (include your API token as <code>X-API-Token</code> in the header). You'll receive 50 days of mango price history and the current price.
                  </li>
                  <li>
                    <strong>Make your trade:</strong> <br />
                    Send a <code>PATCH</code> request to <code>/mean-mangos/session</code> with your <strong>buy/sell</strong> decision and the quantity you want to trade.
                  </li>
                  <li>
                    <strong>See the results:</strong> <br />
                    After 10 days, the final price is revealed and your profit or loss is calculated.
                  </li>
                </ol>
                <details>
                  <summary>Payload Example</summary>
                  <pre><code>// POST request (empty payload)
{}

// PATCH request
{
  "session_id": "abc123",
  "choice": "buy", // buy or sell
  "qty": 10         // positive integer > 1
}</code></pre>
                </details>
                <details>
                  <summary>Response Example</summary>
                  <pre><code>// POST response
{
  "session_id": "abc123",
  "show_price": "50.12;51.03;49.87;...;48.45",  // 50 days of price history
  "entry_price": 48.45                            // Current price for trading
}

// PATCH response
{
  "game_data": {
    "price_data": "50.12;51.03;49.87;...;48.45",  // 50 days of price history
    "entry_price": 48.45,
    "future_price": "49.23;50.12;...;52.34",
    "exit_price": 52.34
  },
  "cost": 484.5,
  "value": 523.4,
  "pnl": 38.9,
  "current_balance": 10038.9
}
</code></pre>
                </details>
                <details>
                  <summary>Error Response</summary>
                  <pre><code>{
  "error": "string"
}</code></pre>
                  <p>Returns HTTP 400 status code with error message if the request is invalid.</p>
                </details>
            </div>
            <div class="goal">
                <h2>Your Mission</h2>
                <p>
                  Study the price swings, trust your instincts, and make your move. Will you spot the pattern or get caught in the swing? Every round is a new challenge—can you maximize your mango profits?
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
    template.value = await getGameTemplate('mean_mangos')
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
