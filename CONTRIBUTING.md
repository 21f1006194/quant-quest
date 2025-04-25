# Contributing to Flask Backend Project

Thank you for your interest in contributing! This guide focuses on getting your contributions merged quickly and efficiently.

## Contribution Process

1. **Find or Create an Issue**
   - Check existing issues first
   - If creating new issue, get an issue number assigned
   - Wait for issue to be approved before starting work

2. **Branch Creation**
   - Branch naming convention: 
     - For features: `feature/#123-short-description`
     - For bugs: `fix/#123-short-description`
     - For docs: `docs/#123-short-description`
     - For refactoring: `refactor/#123-short-description`
   - Where #123 is your issue number
   - Keep the short description concise and descriptive, best to be 2-3 words

3. **Development**
   ```bash
   # Create your branch
   git checkout -b feature/#123-add-user-auth

   # Make your changes and commit
   git add .
   git commit -m "#123: Add user authentication system"
   ```

4. **Early Pull Request**
   - Create PR as soon as you have your first commit
   - Mark it as "Draft" if work is in progress
   - Title format: `[WIP] #123: Add user authentication system`
   - Include "Fixes #123" in PR description to link issue

5. **PR Description Template**
   ```
   Fixes #123

   Changes proposed:
   - Brief point 1
   - Brief point 2

   TODO:
   - [ ] Remaining task 1
   - [ ] Remaining task 2
   ```

## Why Early PRs?

- Get early feedback on approach
- Allow parallel code review
- Prevent wasted effort
- Enable collaboration
- Track progress transparently

## During PR Review

- Reviewers will provide feedback iteratively
- Address feedback in new commits
- Don't force push/rebase until asked
- Keep commits atomic and well-described
- Update PR description as you progress

## Getting Your PR Merged

- All CI checks must pass
- Required reviewers must approve
- PR description must be complete
- Commits should be squashed if requested
- Branch should be up to date with main

## Things to keep in mind while contributing to backend

- All the changes should be done in the `backend` directory.
- All the new APIs should be added to the `routes` directory.
- All the new DB models should be added to the `models` directory.
- All the new common functions should be added to the `utils` directory.
- All the business logic should be added to the `services` directory.

## Things to keep in mind while contributing to frontend

- All the changes should be done in the `frontend` directory.
- Keep the reusable components in the `components` directory.
- Keep the page views in the `views` directory and add them in the `router/index.js` file.
- Use composition API in Vue.js files (i.e., <script setup>).
- Utilize the `api` object from the `services/api.js` to hit any endpoint in the backend.
- Any new services should be added to the `services` directory.
- Make use of the Pinia store to manage state, if needed. Keep any such state management logic in the `stores` directory.
- Use the `authStore` for any authentication related logic.

## Development Environment Setup

1. **Clone the Repository**
   ```bash
   git clone https://github.com/21f1006194/quant-quest.git
   cd quant-quest/backend
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
4. **Setup the environment variables**
    Setup the environment variables in the `.env` files, in both the `backend` and `frontend` directories.

5. **Run the Development Server**
   ```bash
   bash scripts/start.sh
   ```

6. **Setting up the Frontend development environment**
   ```bash
   cd ../frontend
   npm install
   npm run dev
   ```

# How to Add a New Game

## Backend

1. **Create a Game Folder**
   - Add a new folder with the game's name to `backend/app/routes/games`.
   - Follow the file structure of `backend/app/routes/games/game_template`:
     ```
     ├── api.py
     ├── description.md
     ├── engine.py
     ├── __init__.py
     ├── metadata.json
     ├── template.py
     └── utils.py
     ```

2. **File Descriptions**
   - `api.py`: Contains the API endpoints for the game. Use `POST` to start a new session and `PUT` for placing multiple bets in the same session. For stateless games, use `POST` only.
   - `description.md`: Includes the game's description, rules, and API documentation.
   - `engine.py`: Contains the game logic.
   - `template.py`: Provides template code for players to start playing.
   - `utils.py`: Contains utility functions for the game.

3. **Register the Game**
   - Ensure the game and its endpoints are dynamically registered in `backend/app/routes/game_router.py`. (No changes needed in this file)

4. **Update Database Models**
   - Update the database models in `/home/bruce/Desktop/quant-quest/backend/app/models/gameplay.py` as needed. (No changes needed in this file)

5. **Testing**
   - Launch the app (both frontend and backend) and test the game via the frontend.
   - Use the dynamic rendering route `/game/<game_name>/docs` to verify the description and template code.

## Frontend

1. **Verify Documentation Route**
   - Ensure `/game/<game_name>/docs` is functioning as expected.

2. **Create a Game Folder**
   - Add a new folder with the game's name in `/frontend/src/games`.

3. **Game Page**
   - Create a `GamePage.vue` file in the new folder. This will be rendered as the game page for players at `/game/<game_name>`.

4. **Assets**
   - Place any images or assets in the `assets` folder within the game folder.



    
    