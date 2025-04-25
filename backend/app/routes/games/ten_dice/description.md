# Ten Dice

Player bets on a number between 10 and 60.
The house rolls 10 dice.
If the sum of the dice is equal to the player's bet, the player wins  20 times their bet; otherwise, they lose their bet.

## API doc
Here is the curl command to play the game:
```
curl --location --request POST '<base_url>/play/ten_dice' \
--header 'X-API-Token: <api_token>' \
--header 'Content-Type: application/json' \
--data-raw '{
    "choice": <number_between_10_and_60>,
    "bet_amount": <bet_amount>
}'
```

payload:

`choice`: number between 10 and 60

`bet_amount`: number
```

response:

```
{
    "result": {
        "dice_sum": dice_sum,
        "result": win_or_loss,
        "payout": payout
    }
}
```

dice_sum: number
win_or_loss: string
payout: number
