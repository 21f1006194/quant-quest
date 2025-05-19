<template>
  <div class="game-page">
    <img src="@/games/lucky_probability_spin/assets/lucky_spin_cover.jpg" alt="Lucky Probability Spin" class="header-banner" />
    <h1>Lucky Probability Spin</h1>
    <div v-if="gameData" class="game-info">
      <div class="description">
        <h2>Game Description</h2>
        <p>
          Welcome to the <strong>Lucky Probability Spin</strong>—a vibrant game of chance and strategy! A spinning wheel with <em>5 to 8 uniquely sized segments</em> awaits you. Each segment represents a slice of probability. Can you predict where the spin will land?
        </p>
      </div>

      <div class="config">
        <h3>Game Configuration</h3>
        <p>Maximum rounds per user: {{ gameData.max_sessions_per_user }}</p>
        <p>Minimum Bet Amount: {{ gameData.config_data.min_bet }}</p>
        <p>Payout Multiplier: {{ gameData.config_data.payout_multiplier }}</p>
      </div>

      <div class="how-to-play">
        <h2>How to Play</h2>
        <ol>
          <li>
            <strong>Start a round:</strong><br />
            Send a <code>POST</code> request to <code>/play/lucky_probability_spin</code> with no payload, but include your <code>X-API-Token</code> in the header. You’ll receive:
            <ul>
              <li>A <code>session_id</code></li>
              <li>A <code>segments</code> array with segment angles summing to 360°</li>
            </ul>
          </li>
          <li>
            <strong>Make your prediction:</strong><br />
            Send a <code>PATCH</code> request to <code>/play/lucky_probability_spin</code> with:
            <ul>
              <li><code>session_id</code></li>
              <li><code>predicted_segment</code> index (0-based)</li>
              <li><code>bet_amount</code></li>
            </ul>
          </li>
          <li>
            <strong>See the results:</strong><br />
            You’ll get:
            <ul>
              <li>The <code>winning_segment</code></li>
              <li>Your <code>payout</code> and updated <code>balance</code></li>
            </ul>
            Match the segment and win!
          </li>
        </ol>

        <details>
          <summary>Payload Example</summary>
          <pre><code>// POST request (empty)
{}

// PATCH request
{
  "session_id": "abc123",
  "predicted_segment": 3,
  "bet_amount": 10
}</code></pre>
        </details>

        <details>
          <summary>Response Example</summary>
          <pre><code>// POST response
{
  "session_id": "abc123",
  "segments": [90, 45, 60, 75, 90] // degrees, summing to 360
}

// PATCH response
{
  "winning_segment": 3,
  "payout": 20,
  "current_balance": 110
}</code></pre>
        </details>

        <details>
          <summary>Error Response</summary>
          <pre><code>{
  "error": "Invalid session or segment."
}</code></pre>
        </details>
      </div>

      <div class="goal">
        <h2>Your Mission</h2>
        <p>
          Use intuition and calculated risk to choose the segment most likely to win. The probabilities are visible in the angles. Will fortune favor your logic?
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
  template.value = await getGameTemplate('lucky_probability_spin')
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
