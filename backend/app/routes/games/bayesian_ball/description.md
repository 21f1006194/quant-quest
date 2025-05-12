# 🎯 Bayesian Ball

Welcome to **Bayesian Ball** — a game of hidden patterns and smart predictions.

## 🧠 The Setup
- There are **4 bags**: A, B, C, D.
- Each bag has a unique mix of **Red (R), Green (G), and Blue (B)** balls.
- A Bag is picked **randomly** with unknown (non-uniform) probabilities.
- 10 balls are drawn from the bag with replacement, 9 are revealed and 1 is hidden.
- The 10th ball is the **hidden ball** and is the ball you need to predict.
- You will have to predict both the color and the bag used.

## 🎮 How to Play
1. **Start a round**  
   - Send a **POST request**  
   - Get **9 revealed balls** drawn (with replacement) from a hidden bag.

2. **Make your prediction**  
   - Send a **PATCH request** with:
     - Your guess for the **10th ball's color**
     - Your guess for the **bag used**

3. **View results**  
   - Response will reveal:
     - The **actual 10th ball color**
     - The **correct bag**
     - Your **payout info**

✅ You win if **both** the color and bag predictions are correct.

## 🔍 Goal
Observe, infer, and adapt. Use logic and Bayesian probability to **maximize your winnings**.

Ready to beat the odds?
