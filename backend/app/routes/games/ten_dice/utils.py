def validate_bet_data(bet_data):
    # check for choice to be an integer between 10 and 60
    if "choice" not in bet_data or "bet_amount" not in bet_data:
        raise ValueError("Bet data must contain choice and bet_amount")
    if bet_data["choice"] not in range(10, 60):
        raise ValueError("Invalid bet data")
    return True
