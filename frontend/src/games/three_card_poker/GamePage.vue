<!-- 3 Card Poker -->
<template>
  <div class="game-page">
    <img src="@/games/three_card_poker/assets/three_card_poker_cover.jpg" alt="Three Card Poker Cover" class="header-banner" />
    <h1>Three Card Poker</h1>
    <div class="game-info">
      <div class="description">
        <h2>Game Description</h2>
        <p>
          Welcome to <strong>Three Card Poker – QuantQuest Edition!</strong> <br>
          Experience the thrill of a fast-paced poker variant where strategy meets luck! In this exciting game, you'll face off against the dealer in a battle of wits and chance. Each round, you'll receive three cards from a standard 52-card deck, and your mission is simple: build a stronger poker hand than the dealer's.
        </p>
        <p>
          What makes this game special? It's the perfect blend of quick decision-making and strategic betting. You'll need to think on your feet as you decide whether to fold or raise after seeing your cards. With five rounds per session, each hand brings new opportunities to test your poker skills and intuition.
        </p>
        <p>
          <strong>New to Poker?</strong> Don't worry! Scroll down to the "Hand Rankings" section below to learn how different card combinations are valued and how winners are determined. Understanding these rankings is key to making smart betting decisions!
        </p>
        <p>
          <strong>Key Features:</strong>
          <ul>
            <li>Fast-paced gameplay with quick rounds</li>
            <li>Simple yet strategic betting system</li>
            <li>Clear hand rankings that are easy to understand</li>
            <li>Memory element as cards aren't returned to the deck during the session</li>
            <li>Perfect for both beginners and experienced players</li>
          </ul>
        </p>
      </div>
      <div class="how-to-play">
        <h2>How to Play</h2>
        <ol>
          <li>
            <strong>Start a Game:</strong> Begin a session (5 rounds per session).
          </li>
          <li>
            <strong>Place Your Bet:</strong> Bet to see your 3 cards.
          </li>
          <li>
            <strong>Decide:</strong> Look at your cards and choose to <b>fold</b> (give up your bet) or <b>raise</b> (bet again to challenge the dealer).
          </li>
          <li>
            <strong>Reveal:</strong> If you raise, the dealer's cards are shown. The stronger hand wins!
          </li>
          <li>
            <strong>Repeat:</strong> Play all 5 rounds and see how much you can win!
          </li>
        </ol>
        <p>
          <b>Tip:</b> Cards aren't returned to the deck during your session, so remembering what's been played can help you win more!
        </p>
      </div>
      <div class="hand-rankings">
        <h2>Hand Rankings (Best to Worst)</h2>
        <ul>
          <li><b>Straight Flush:</b> Three cards in a row, all the same suit (e.g., 9♠ 10♠ J♠)</li>
          <li><b>Three of a Kind:</b> All three cards are the same number or face (e.g., Q♦ Q♣ Q♠)</li>
          <li><b>Straight:</b> Three cards in a row, any suits (e.g., 4♦ 5♠ 6♣)</li>
          <li><b>Flush:</b> Three cards, all the same suit (e.g., 2♥ 8♥ K♥)</li>
          <li><b>Pair:</b> Two cards with the same number or face (e.g., 7♣ 7♦ K♠)</li>
          <li><b>High Card:</b> None of the above—just the highest card wins (e.g., A♠ 10♣ 6♦)</li>
        </ul>
        <p>
          <i>If you and the dealer have the same type of hand, the highest card wins!</i>
        </p>
      </div>
      <div class="api-how-to-play">
        <details>
          <summary>API How-To</summary>
          <ol>
            <li>
              <b>POST</b> to <code>/play/three_card_poker</code> to start a session. Save the <code>session_id</code>.
            </li>
            <li>
              <b>PATCH</b> with <code>session_id</code> and <code>base_bet</code> to get your cards. Save the <code>bet_id</code>.
            </li>
            <li>
              <b>PATCH</b> again with <code>session_id</code>, <code>bet_id</code>, and <code>raise_bet</code> (0 to fold, or your raise amount).
            </li>
            <li>
              Repeat last 2 steps for all 5 rounds!
            </li>
          </ol>
        </details>
      </div>
      <details>
        <summary>Python Template</summary>
        <PythonTemplate v-if="template" :code="template" game_name="three_card_poker" />
      </details>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getGameTemplate } from '@/services/gameService'
import PythonTemplate from '@/components/game/PythonTemplate.vue'

const template = ref(null)

onMounted(async () => {
  template.value = await getGameTemplate('three_card_poker')
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
.hand-rankings ul {
  margin-left: 1.5em;
}
.api-how-to-play {
  margin-top: 2em;
}
</style>
    
