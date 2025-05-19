# 🎲 Three Doors Maze

**Three Doors Maze** is a stateful betting game where players navigate through a randomly generated maze by choosing between three doors — A, B, or C — at each step. The goal is to reach the final room and claim a payout!

---

## 🚪 Gameplay Summary

- At each room, you choose one of three doors.
- Each door has a **hidden success probability** to reach the next room.
- If the door succeeds, you move forward. If not, you stay and try again.
- You receive **probabilistic hints** to help guide your decision.
- You have limited attempts per door — plan wisely!
- Reach the final room to win a payout (default: `bet × 5`).

---

## 🧠 Technical Overview

- The maze is a **ternary DAG (Directed Acyclic Graph)**:
  - Each room has 3 doors (edges) leading to different rooms.
  - Random **cross-connections** can link back to previous rooms.
- **Success probabilities** per door are randomly generated.
- The game uses **Bayesian updating** to refine the player's belief about door success as more outcomes are revealed.
- Game state is persistent via sessions; players can continue unfinished games.

---