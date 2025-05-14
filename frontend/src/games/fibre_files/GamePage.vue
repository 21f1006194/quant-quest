<template>
  <div class="game-page">
    <img src="@/games/fibre_files/assets/fibre_files_cover.jpg" alt="fibre files" class="header-banner" />
    <h1>The Fibre Files</h1>
    <div v-if="gameData" class="game-info">
      <div class="description">
        <h2>Game Description</h2>
        <p v-html="renderedDescription"></p>
      </div>

      <div class="config">
        <h3>Game Configuration</h3>
        <p>Maximum bets per user: {{ gameData.max_sessions_per_user }}</p>
        <p>Payout: {{ gameData.config_data.payout }}</p>
      </div>

      <div class="how-to-play">
        <h2>How to Play</h2>
        <ol>
          <li>
            <strong>Start the Game:</strong><br />
            Send a <code>POST</code> request to <code>/play/fibre_files</code> with your suspect choice and bet. Include your API token as <code>X-API-Token</code> in the header.
          </li>
          <li>
            <strong>Analyze the Outcome:</strong><br />
            The response reveals the result of your guess and your current wallet balance.
          </li>
        </ol>

        <details>
          <summary>Payload Example</summary>
          <pre><code>// POST request
{}
// PATCH request
{
  "session_id": "string",
  "choice": number between 0 and 9,
  "bet_amount": number
}</code></pre>
              </details>

              <details>
                <summary>Response Example</summary>
                <pre><code>// POST response
 {

  // PATCH response
  "result": {
    // Game specific result data
  },
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
          Dive into the mystery of <strong>The Fibre Files</strong>. With 10 suspects and limited clues, can you deduce who’s behind the riddle? Use logic, strategy, and a bit of luck to solve the case and maximize your winnings!
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
  template.value = await getGameTemplate('fibre_files')
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
