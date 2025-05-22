# 🎲 Biased Coin Toss Game

> A simple, stateless, single-trial betting game used for system compatibility testing and user onboarding demos.

---

## 🧠 Game Concept

The system tosses a **biased coin** internally. You must **bet on either "H" (Heads) or "T" (Tails)**. If your prediction is correct, you win a payout!

This game is designed to:
- Be quick and intuitive
- Demonstrate API session and bet handling
- Be used in demo videos and onboarding trials

---

## ⚙️ Game Rules

- You can **only bet once per session**
- Minimum bet: **10 units**
- Payout multiplier: **1.7x**

---

## 🔁 Game Flow (API)

### 1. `POST /play/coin_toss` 

Tosses a biased coin and returns the session_id.

### 2. `PATCH /play/coin_toss`

Places a bet on the same session_id.

