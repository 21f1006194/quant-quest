# 📘 Modular Database Schema Documentation

[View Interactive Diagram on dbdiagram.io](https://dbdiagram.io/d/quantix-schema-design-67f278c94f7afba18483d18f)


This backend is designed for a game-based platform involving users, game sessions, bets, wallet transactions, and user management. The schema is fully modular and scalable for future growth.

## Email Validation Format

Only institute-issued IITM Data Science emails are allowed:

```regex
^\d{2}f\d{7}@ds\.study\.iitm\.ac\.in$
```

---

## 📁 Database Schema Overview

### 1. `users` – Core User Table

| Field                  | Type         | Description                      |
| ---------------------- | ------------ | -------------------------------- |
| `id`                   | Integer (PK) | Unique user ID                   |
| `email`                | String (120) | Unique IITM email ID (validated) |
| `username`             | String (80)  | Unique username                  |
| `password_hash`        | String (256) | Hashed password                  |
| `full_name`            | String (100) | User's full name                 |
| `is_admin`             | Boolean      | Whether the user is an admin     |
| `created_at`           | DateTime     | Timestamp of account creation    |
| `api_token`            | String (64)  | API token for authentication     |
| `api_token_created_at` | DateTime     | When the token was generated     |

#### Relationships:
- One-to-One → `Wallet`
- One-to-Many → `VerificationToken`
- One-to-Many → `GameSession`

---


### 2. `verification_tokens` – Secure Token Management

| Field        | Type         | Description                                  |
| ------------ | ------------ | -------------------------------------------- |
| `id`         | Integer (PK) | Token ID                                     |
| `user_id`    | Integer (FK) | Belongs to a user                            |
| `token`      | String(128)  | Secure random token                          |
| `purpose`    | String(50)   | e.g., `email_verification`, `password_reset` |
| `expires_at` | DateTime     | Expiry timestamp                             |
| `created_at` | DateTime     | Creation time                                |
| `is_used`    | Boolean      | Whether the token was already used           |

---

### 3. `wallets` – Virtual Wallet System

| Field          | Type         | Description                     |
| -------------- | ------------ | ------------------------------- |
| `id`           | Integer (PK) | Wallet ID                       |
| `user_id`      | Integer (FK) | One-to-one with user            |
| `balance`      | Float        | Wallet balance (default 0.0)    |
| `currency`     | String(10)   | Currency code (e.g., INR)       |
| `last_updated` | DateTime     | Timestamp of last wallet update |

#### Relationships:
- One-to-Many → `Transaction`

---

### 4. `transactions` – Wallet Transaction Log

| Field         | Type            | Description                                      |
| ------------- | --------------- | ------------------------------------------------ |
| `id`          | Integer (PK)    | Transaction ID                                   |
| `wallet_id`   | Integer (FK)    | Belongs to a wallet                              |
| `amount`      | Float           | Transaction amount                               |
| `type`        | Enum            | `credit` or `debit`                              |
| `category`    | Enum (optional) | `bet`, `win`, `bonus`, `admin_adjustment`        |
| `description` | String(255)     | Optional human-readable label                    |
| `metadata`    | JSON            | Optional reference data (e.g., admin, game info) |
| `created_at`  | DateTime        | Time of creation                                 |
| `updated_at`  | DateTime        | Auto-updated on change                           |
| `deleted_at`  | DateTime        | Soft-delete field                                |

#### Indexes:
- `wallet_id`
- `category`
- `created_at`

---

### 5. `games` – Game Metadata

| Field         | Type         | Description                          |
| ------------- | ------------ | ------------------------------------ |
| `id`          | Integer (PK) | Game ID                              |
| `name`        | String(100)  | Unique game name                     |
| `description` | Text         | Game description                     |
| `type`        | String(50)   | E.g., `quiz`, `puzzle`, `prediction` |
| `metadata`    | JSON         | Game-specific configuration          |
| `created_at`  | DateTime     | Game creation timestamp              |

#### Relationships:
- One-to-Many → `GameSession`

---

### 6. `game_sessions` – Tracks Gameplay

| Field        | Type         | Description                                   |
| ------------ | ------------ | --------------------------------------------- |
| `id`         | Integer (PK) | Session ID                                    |
| `user_id`    | Integer (FK) | Player reference                              |
| `game_id`    | Integer (FK) | Game being played                             |
| `started_at` | DateTime     | Session start                                 |
| `ended_at`   | DateTime     | Session end                                   |
| `duration`   | Interval     | Total time spent                              |
| `result`     | String(20)   | E.g., `win`, `loss`, `draw`                   |
| `score`      | Float        | Score obtained                                |
| `status`     | String(20)   | E.g., `in_progress`, `completed`, `forfeited` |
| `metadata`   | JSON         | Gameplay data like level, stage, etc.         |

#### Relationships:
- One-to-Many → `Bet`

---

### 7. `bets` – In-Game Betting

| Field           | Type         | Description                         |
| --------------- | ------------ | ----------------------------------- |
| `id`            | Integer (PK) | Bet ID                              |
| `session_id`    | Integer (FK) | Linked to a game session            |
| `amount`        | Float        | Amount wagered                      |
| `placed_at`     | DateTime     | When the bet was placed             |
| `outcome`       | String(20)   | E.g., `win`, `loss`                 |
| `payout`        | Float        | Resulting money change              |
| `choice`        | String(100)  | The user's chosen answer/prediction |
| `is_successful` | Boolean      | Whether the bet was successful      |
| `metadata`      | JSON         | Odds, context, etc.                 |

---

