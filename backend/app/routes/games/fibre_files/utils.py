def validate_bet_data(bet_data, config):
    if "choice" not in bet_data or "bet_amount" not in bet_data:
        raise ValueError("Missing bet data")
    if bet_data["choice"] not in range(0, 10):
        raise ValueError("Choice must be between 0 and 9")
    return True
