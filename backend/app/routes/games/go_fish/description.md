# Go Fish

## Description

Player is given 7 cards randomly in the begining of the game. Then the player is asked to guess the next card. If the guess is correct, then player wins 4x the bet amount, if the guess is half correct then player wins 1.5x the bet amount. If the guess is wrong, they looses the bet amount. Players are allowed to do 7 such guesses within a game.


- empty post request to get the initial 7 cards and session id of the game,
- patch request to place the bet, with bet amount and choice of card.