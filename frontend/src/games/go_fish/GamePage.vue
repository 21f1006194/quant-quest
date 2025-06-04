<template>
    <div class="game-page">
        <img src="@/games/go_fish/assets/go_fish_cover.jpg" alt="Go Fish" class="header-banner" />
        <h1>Go Fish</h1>
        <div v-if="gameData" class="game-info">
            <div class="description">
                <h2>Game Description</h2>
                <p>
                    Welcome to <strong>Go Fish</strong>—an exciting card game where you test your prediction skills! At the start of each game, you'll receive 7 random cards. Your challenge is to predict the next card that will be drawn from the deck.
                </p>
                <p>
                    The game offers multiple opportunities to win:
                    <ul>
                        <li>If you guess the exact card (both suit and rank), you win 6x your bet amount!</li>
                        <li>If you guess either the suit or rank correctly (half correct), you win 2x your bet amount</li>
                        <li>If your guess is completely wrong, you lose your bet amount</li>
                    </ul>
                </p>
                <p>
                    You can make up to 7 predictions in each game session. Each prediction is a chance to increase your winnings or recover from previous losses. Will you play it safe or go for the big win?
                </p>
            </div>
            <div class="config">
                <h3>Game Configuration</h3>
                <p>Maximum bets per session: {{ gameData.max_bets_per_session }}</p>
                <p>Full guess payout: 6x</p>
                <p>Half guess payout: 2x</p>
                <p>Minimum Bet amount : 30</p>
            </div>
            <div class="how-to-play">
                <h2>How to Play</h2>
                <ol>
                  <li>
                    <strong>Start a game:</strong> <br />
                    Send a <code>POST</code> request to <code>/play/go_fish</code> (include your API token as <code>X-API-Token</code> in the header). You'll receive 7 initial cards and a session ID to track your game.
                  </li>
                  <li>
                    <strong>Make your prediction:</strong> <br />
                    Send a <code>PATCH</code> request to <code>/play/go_fish</code> with your guess for the next card, your bet amount, and the session ID.
                  </li>
                  <li>
                    <strong>See the results:</strong> <br />
                    The response will reveal the drawn card and your payout information. You can continue making predictions until you've used all 7 attempts or choose to start a new game.
                  </li>
                </ol>
                <details>
                  <summary>Payload Example</summary>
                  <pre><code>// POST request (empty payload)
{}

// PATCH request
{
  "session_id": "string",
  "choice": "string",    // Card choice (e.g., "AH" for Ace of Hearts)
  "bet_amount": number
}</code></pre>
                </details>
                <details>
                  <summary>Response Example</summary>
                  <pre><code>// POST response
{
  "session_id": number,
  "initial_cards": string[]  // Array of 7 cards
}

// PATCH response
{
  "bet_id": number,
  "fishing_count": number,
  "result": {
    "card": string,
    "payout": number
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
                  Use your knowledge of probability and card counting to make the best predictions. Each game is a new opportunity to test your skills and maximize your winnings. Can you become the Go Fish champion?
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
    template.value = await getGameTemplate('go_fish')
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
