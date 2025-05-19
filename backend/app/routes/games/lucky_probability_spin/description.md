#  Lucky Probability Spin

Spin the wheel, pick a color, and test your luck with probability and expected value insights!

## Final Game Design

| Segment (Color) | Angle (°) | Probability (%) | Payout (Points) |
|------------------|------------|-------------------|---------------------|
| Red              | 36°        | 10%               | 100                 |
| Blue             | 54°        | 15%               | 75                  |
| Green            | 90°        | 25%               | 50                  |
| Yellow           | 108°       | 30%               | 25                  |
| Purple           | 72°        | 20%               | 40                  |
| **Total**        | 360°       | 100%              |                     |

## Expected Value
\[
EV = \sum (\text{probability} \times \text{payout}) = 49.25 \text{ points}
\]

## API
- **POST** `/api/lucky_spin/`
  - Request: `{ "choice": "Red" }`
  - Response:
    ```json
    {
        "result": "Blue",
        "payout": 0,
        "won": false,
        "expected_value": 49.25
    }
    ```
