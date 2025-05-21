# 🥭 Mean Mangos

In a small market town, mango prices have been moving unpredictably for weeks — sometimes climbing, sometimes falling. You've been tracking the price for 50 days, and now it's your chance to make a move.

Based on what you've seen, decide whether to **buy** or **sell** mangos, and choose how much you want to trade. Ten days later, you'll find out how your decision played out.

Some say mango prices have a way of finding their balance.
Will you spot the pattern — or get caught in the swing?

---

## 🎮 How to Play

1. **Get the Price History**
   Start a new game session to receive 50 days of historical price data.

2. **Analyze the Trend**
   Study the price movements carefully. Look for patterns that might help predict future prices.

3. **Make Your Move**
   Decide whether to **buy** or **sell**, and choose how many units you're willing to trade.

4. **See the Outcome**
   After 10 days, the final price is revealed, and your profit or loss is calculated.

---

## 🧪 API

### 1. Start a New Game

```http
POST /play/mean-mangos
```

**Response:**

```json
{
  "session_id": "abc123",
  "show_price": "50.12;51.03;49.87;...;48.45",  // 50 days of price history
  "entry_price": 48.45,                         // Current price for trading
}
```

---

### 2. Submit Your Trade

```http
PATCH /mean-mangos/session
```

**Payload:**

```json
{
  "session_id": "abc123",
  "choice": "buy",         // buy or sell
  "qty": 10           // positive integer > 1
}
```

**Response:**

```json
{
  "game_data": {
    "price_data": "50.12;51.03;49.87;...;48.45",  // 50 days of price history
    "entry_price": 48.45,
    "future_price": "49.23;50.12;...;52.34",
    "exit_price": 52.34
  },
  "cost": <number>,
  "value": <number>,
  "pnl": <number>,
  "current_balance": <number>
}
```
