# Triple-or-Nothing Flip 🎲

## Overview
A two-step high-risk, high-reward coin flip game designed to test system compatibility and introduce risk-reward decision-making.

### Game Flow
1. **Initial Bet**: The player starts by betting an amount `x`.
2. **First Flip**:
   - If **Heads (H)**: Player wins `x` and may proceed to the second flip.
   - If **Tails (T)**: Player loses `x`, and the game ends.
3. **Second Flip (Optional)**:
   - If **Heads (H)**: Player wins `3x`.
   - If **Tails (T)**: Player loses everything (total payout = `0`).

### Characteristics
- Stateless, transactional gameplay
- 50/50 fair coin
- Max 1 bet per session
- Tags: `coin`, `flip`, `risk`, `demo`

## Example
- Bet ₹10 → Flip1: H → Flip2: H → Winnings: ₹30
- Bet ₹10 → Flip1: H → Flip2: T → Winnings: ₹0
- Bet ₹10 → Flip1: T → Winnings: ₹0

## API Endpoints
- `GET /play/triple_or_nothing`: Get game config
- `POST /play/triple_or_nothing`: Start new flip session
- `PATCH /play/triple_or_nothing`: Place bet and optionally proceed to second flip
