# 🃏 **Three Card Poker – QuantQuest Edition**

**Description:**
A fast-paced game where you and the dealer are each dealt **3 cards** from a standard 52-card deck. Your goal is to build a stronger **poker hand** than the dealer. Think fast, bet smart, and outplay across **5 rounds** in a session.

---

**Hand Rankings (Highest to Lowest):**
Three-card poker has simplified hand rankings compared to five-card poker:

1. **Straight Flush** – Three consecutive cards of the same suit (e.g., `9♠ 10♠ J♠`)
2. **Three of a Kind** – Three cards of the same rank (e.g., `Q♦ Q♣ Q♠`)
3. **Straight** – Three consecutive cards of mixed suits (e.g., `4♦ 5♠ 6♣`)
4. **Flush** – Three cards of the same suit (e.g., `2♥ 8♥ K♥`)
5. **Pair** – Two cards of the same rank (e.g., `7♣ 7♦ K♠`)
6. **High Card** – None of the above; highest single card determines the hand (e.g., `A♠ 10♣ 6♦`)

✅ **Ties are broken** by comparing the highest cards in the hand, then the second, then third if needed.

---

**Gameplay:**
Each game session includes **5 rounds**. In each round:

* You place a **base bet** to see your 3-card hand.
* Then choose to **fold** (forfeit the base bet) or **bet again** to challenge the dealer.
* If you play, the **dealer's hand is revealed** and the higher-ranked hand wins.

📌 **Strategic Tip:** Cards are **not returned to the deck** during the session, so memory and card-counting give you an edge in later rounds.

**How to play:**

1. **Start a Game Session**
   - Send a POST request to `/play/three_card_poker`
   - Save the `session_id` from the response
   - Each session consists of 5 rounds

2. **Place Base Bet**
   - Send a PATCH request with:
     - `session_id` from step 1
     - `base_bet` amount
   - Save the `bet_id` and your `hand` from the response

3. **Make Your Move**
   - Send a PATCH request with:
     - `session_id` from step 1
     - `bet_id` from step 2
     - `raise_bet`: 
       - Set to 0 to fold
       - Set to your desired amount to raise
   - The response will show:
     - Dealer's hand
     - Your total bet
     - Payout (if any)
     - Updated balance

Repeat steps 2-3 for each of the 5 rounds in your session.