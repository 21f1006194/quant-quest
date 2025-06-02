<template>
    <div class="game-page">
        <img src="@/games/final_draw/assets/final_draw_cover.jpg" alt="Final Draw" class="header-banner" />
        <h1>Final Draw Challenge</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>
                    Welcome to the Final Draw Challenge! You'll be playing with a deck of cards, each with its own unique value.
                    You'll be shown cards one at a time, and you must decide whether to select the current card or skip to the next one.
                    Once you select a card, that's your final choice - you can't go back to previous cards!
                </p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum rounds per user: {{ gameData.max_sessions_per_user }}</p>
                <p>Minimum bet: 1 unit</p>
            </div>
            <div class="how-to-play">
                <h2>How to Play</h2>
                <ol>
                  <li>
                    <strong>Start a round:</strong> <br />
                    Send a <code>POST</code> request to <code>/play/final_draw</code> with your API token in the header.
                  </li>
                  <li>
                    <strong>Make your choice:</strong> <br />
                    Send a <code>PATCH</code> request to <code>/play/final_draw</code> with your decision to select or skip the current card.
                  </li>
                  <li>
                    <strong>Check the game state:</strong> <br />
                    Send a <code>GET</code> request to <code>/play/final_draw</code> to see the current card and session status.
                  </li>
                </ol>
                <details>
                  <summary>Request Details</summary>
                  <pre><code>// POST request (empty payload)
{}

// PATCH request
{
  "session_id": "number",    // Session ID from POST response
  "choice": "string"        // "select" to keep current card or "skip" for next card
}

// GET request (no payload needed)</code></pre>
                </details>
                <details>
                  <summary>Response Details</summary>
                  <pre><code>// POST response
{
  "session_id": number,
  "last_pick": number,      // Value of the drawn card
  "message": "Continue the game"
}

// PATCH response
{
  "session_id": number,
  "last_pick": number,      // Value of the current/last drawn card
  "bet_id": number,         // ID of the bet placed
  "bet_count": number,      // Number of bets in this session
  "current_balance": number // Your updated balance
}

// GET response
{
  "session_id": number,
  "last_pick": number      // Value of the current card
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
                  Watch the cards carefully and make strategic decisions. 
                  Each card you see could be your final choice, so choose wisely!
                  Can you maximize your score by selecting the best card at the right moment?
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
    template.value = await getGameTemplate('final_draw')
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
