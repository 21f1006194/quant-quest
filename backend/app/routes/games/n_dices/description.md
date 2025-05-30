# **N Dice**

## **Game Description**

In **N Dice**, the number of dice `n` is randomly chosen by the server at the beginning of each round.

1. The player starts by making an empty POST request to the game endpoint to fetch the number of dice `n` for that round.
2. After receiving the value of `n`, the player bets on a number between `n` and `6 * n` (the minimum and maximum possible sum of `n` dice).
3. The house rolls `n` dice.
4. If the sum of the dice matches the player’s guess, the player wins **20 times** their bet; otherwise, they lose their bet.

---

## **API Documentation**

### **1. Get number of dice**

To start a new round and fetch the number of dice:

```bash
curl --location --request POST '<base_url>/play/n_dice' \
--header 'X-API-Token: <api_token>'
```

**Response:**

```json
{
    "session_id": <session_id>,
    "n": <number_of_dice>
}
```

---

### **2. Play the game**

After receiving `n`, place a bet with your guessed sum:

```bash
curl --location --request POST '<base_url>/play/n_dice' \
--header 'X-API-Token: <api_token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "choice": <number_between_n_and_6n>,
    "bet_amount": <bet_amount>
}'
```

**Payload Fields:**

* `choice`: Integer between `n` and `6 * n` (your guess for the total dice sum)
* `bet_amount`: Number (the amount you are betting)

---

### **Response:**

```json
{
    "result": {
        "dice_sum": <sum_of_dice>,
        "result": "win" | "loss",
        "payout": <number>
    },
    "current_balance": <current_balance>
}
```

* `dice_sum`: The total sum rolled with `n` dice
* `result`: "win" if your guess was correct, otherwise "loss"
* `payout`: payout amount if win, 0 if loss
* `current_balance`: the player's current balance after the bet
