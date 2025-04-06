# 📘 Modular Database Schema Documentation

This modular schema design manages user accounts, verification flows, gameplay, wallets, and transactions. Each module is housed in separate files for scalability and clarity.

---

## 📂 Modules Overview

- **user.py**: Core user authentication, email verification, and account status management.
- **profile.py**: Extended profile fields - for enhanced UI.
- **verification.py**: Email/password verification token management.
- **wallet.py**: Wallet and transaction tracking.
- **gameplay.py**: Game sessions, bets, and gameplay data.

---

## 📑 Table Descriptions

<details>
<summary>🧑 <strong>users</strong></summary>

Stores core user identity and authentication data.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer, PK | Unique user ID |
| `roll_number` | String(10), Unique | Institute roll number |
| `email` | String(120), Unique | IITM academic email |
| `username` | String(50), Unique | User’s handle |
| `full_name` | String(100) | Full name |
| `password_hash` | String(256) | Hashed password |
| `is_active` | Boolean | User status |
| `email_verified` | Boolean | Email verification flag |
| `failed_login_attempts` | Integer | Brute-force protection |
| `last_login` | DateTime | Last login time |
| `api_token` | String(64) | Session API token |
| `api_token_created_at` | DateTime | Token issue time |
| `created_at` | DateTime | Account creation timestamp |

🔁 **Relationships**:
- One-to-Many: `VerificationToken`
- One-to-One: `UserProfile`, `Wallet`

</details>

---

<details>
<summary>✅ <strong>verification_tokens</strong></summary>

Manages one-time tokens for user actions.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer, PK | Token ID |
| `user_id` | Integer, FK (`users.id`) | Owner |
| `token` | String(128) | Unique token |
| `purpose` | String(50) | Reason (e.g., email_verification, reset) |
| `expires_at` | DateTime | Expiry time |
| `created_at` | DateTime | Issued time |
| `is_used` | Boolean | Has the token been used? |
</details>

---

<details>
<summary>👤 <strong>user_profiles</strong></summary>

Stores additional user profile info.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer, PK | Profile ID |
| `user_id` | Integer, FK (`users.id`), Unique | Owner |
| `bio` | Text | Optional biography |
| `avatar_url` | String(255) | Profile image |
| `location` | String(100) | Geographic location |
| `dob` | Date | Date of birth |
| `created_at` | DateTime | Creation time |
| `updated_at` | DateTime | Last update |
</details>

---

<details>
<summary>💰 <strong>wallets</strong></summary>

Each user gets one wallet for game transactions.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer, PK | Wallet ID |
| `user_id` | Integer, FK (`users.id`), Unique | Owner |
| `balance` | Float | Current funds |
| `last_updated` | DateTime | Last balance update |

🔁 One-to-Many: `transactions`
</details>

---

<details>
<summary>💸 <strong>transactions</strong></summary>

Tracks wallet transactions.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer, PK | Transaction ID |
| `wallet_id` | Integer, FK (`wallets.id`) | Linked wallet |
| `amount` | Float | Transaction value |
| `type` | String(20) | "credit" or "debit" |
| `category` | String(50) | Reason (e.g., bet, win, top-up) |
| `description` | String(255) | Notes |
| `created_at` | DateTime | Transaction time |
</details>

---

<details>
<summary>🎮 <strong>games</strong></summary>

Game definition for the platform.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer, PK | Game ID |
| `name` | String(100) | Game title |
| `description` | Text | What it is |
| `created_at` | DateTime | Entry creation |
</details>

---

<details>
<summary>🕹️ <strong>game_sessions</strong></summary>

Tracks game sessions started by users.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer, PK | Session ID |
| `user_id` | Integer, FK (`users.id`) | Player |
| `game_id` | Integer, FK (`games.id`) | Game played |
| `started_at` | DateTime | Start time |
| `ended_at` | DateTime | End time |
</details>

---

<details>
<summary>🎯 <strong>bets</strong></summary>

Betting or interaction records inside sessions.

| Field | Type | Description |
|-------|------|-------------|
| `id` | Integer, PK | Bet ID |
| `session_id` | Integer, FK (`game_sessions.id`) | Parent session |
| `amount` | Float | Bet amount |
| `result` | String(20) | Outcome |
| `created_at` | DateTime | When the bet was placed |
</details>

---

## 🔗 Relationship Map

- `User` ↔ `UserProfile`: One-to-One
- `User` ↔ `VerificationToken`: One-to-Many
- `User` ↔ `Wallet`: One-to-One
- `Wallet` ↔ `Transaction`: One-to-Many
- `Game` ↔ `GameSession`: One-to-Many
- `GameSession` ↔ `Bet`: One-to-Many

---

## 🔧 Adjustments Made

- Removed MFA from the schema (since it's not essential)
- Streamlined the user model and email validation, avoiding complexity like roles.
- Removed unnecessary audit log models.
- Verified Delete Cascade Integrities.

---