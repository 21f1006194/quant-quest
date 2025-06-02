# Final Draw Challenge

## Description

A deck of cards is shuffled and the user is given a chance to draw a card. These cards have different values and the user can stop drawing at any time. The user will get the value of the card they stopped at. User cannot choose a previous, the last card is the only card that can be chosen.

## Game Flow

### 1. `POST /play/final_draw`

Returns a session_id. and the initial card drawn "last_pick"

### 2. `PATCH /play/final_draw`

Places a bet on the same session_id, and choose to select or skip the "last_pick", if skipped, the next card is drawn and the process continues.

### 3. `GET /play/final_draw`

Returns the final card drawn "last_pick" and the session_id.





