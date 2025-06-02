# 🎲 Signal Sequence Game

## Description

Signal Sequence is a single-player, stateful puzzle game where players decode a hidden sequence of five colored signal lights—Red, Blue, Green, Yellow, and Purple—each selected from a subtly biased probability distribution. The signals turn on one by one, and the player must predict each color in the correct order to build a streak. With each correct guess, the next light activates; a single mistake ends the round. The core challenge lies in detecting the hidden color distribution across multiple games and leveraging that knowledge to outperform chance. Signal Sequence rewards players who use statistical reasoning and pattern recognition to gain a probabilistic edge in an otherwise uncertain environment.


## Game Flow

### 1. `POST /play/signal_sequence`

Starts a new game session and returns the session_id.

### 2. `PATCH /play/signal_sequence`

Places a bet on the same session_id, with the bet_amount and choice.
Keep placing the bet until your guess is wrong or maximum upto four bets.

