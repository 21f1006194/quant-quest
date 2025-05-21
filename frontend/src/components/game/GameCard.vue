<template>
    <div class="game-card">
        <div class="game-content">
            <div class="game-main">
                <div class="main-row">
                    <h3 class="game-name">{{ formattedName }}</h3>
                    <div class="session-row">
                        <i class="bi bi-controller"></i>
                        <span>{{ attemptsRemaining }}/{{ maxAttempts }}</span>
                    </div>
                </div>
                <div class="info-row">
                    <div class="tags">
                        <span class="difficulty-tag" :class="difficulty.toLowerCase()">{{ difficulty }}</span>
                        <span v-for="tag in tagList" :key="tag" class="tag">{{ tag }}</span>
                    </div>
                    <span v-if="maxBets > 1" class="bets-pill">Bets/session: {{ maxBets }}</span>
                </div>
            </div>
            <div class="game-side">
                <div class="side-row">
                    <div class="pnl" :class="{ 'positive': pnl > 0, 'negative': pnl < 0 }">
                        <span class="pnl-label">PnL</span>
                        <span class="pnl-value">{{ pnl }}</span>
                    </div>
                    <router-link :to="`/game/${gameName}`" class="play-button" :title="`Play ${formattedName}`">
                        <i class="bi bi-play-btn-fill"></i>
                    </router-link>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
    gameName: {
        type: String,
        required: true
    },
    maxSessions: {
        type: Number,
        required: true
    },
    sessionsUsed: {
        type: Number,
        required: true
    },
    maxBets: {
        type: Number,
        required: true
    },
    difficulty: {
        type: String,
        required: true
    },
    tags: {
        type: String,
        required: true
    },
    pnl: {
        type: Number,
        required: true
    }
});

const formattedName = computed(() => {
    return props.gameName
        .replace(/_/g, ' ')
        .split(' ')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
});

const tagList = computed(() => {
    return props.tags.split(',').map(tag => tag.trim());
});

const attemptsRemaining = computed(() => {
    return props.maxSessions - props.sessionsUsed;
});

const maxAttempts = computed(() => props.maxSessions);
const maxBets = computed(() => props.maxBets);
</script>

<style scoped>
.game-card {
    background: var(--card-dark);
    border-radius: var(--border-radius-md);
    padding: 1rem 1.5rem;
    margin: 0.5rem 0;
    width: 60vw;
    max-width: 1100px;
    min-width: 320px;
    box-shadow: var(--shadow-sm);
    border: 1px solid rgba(100,255,218,0.08);
    transition: box-shadow var(--transition-fast), border-color var(--transition-fast);
}
@media (max-width: 900px) {
    .game-card {
        width: 98vw;
        max-width: 100vw;
        min-width: 0;
        padding: 0.7rem 0.5rem;
    }
}
.game-card:hover {
    box-shadow: var(--shadow-md);
    border-color: var(--primary-color);
}
.game-content {
    display: flex;
    justify-content: space-between;
    align-items: center;
    gap: 1.2rem;
}
.game-main {
    flex: 1;
    min-width: 0;
}
.main-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.2rem;
}
.game-name {
    margin: 0;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--primary-color);
    letter-spacing: 0.01em;
    line-height: 1.1;
}
.session-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.3rem;
    font-size: 0.98rem;
    color: var(--secondary-color);
}
.session-row i {
    font-size: 1rem;
    color: var(--primary-color);
}
.info-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.1rem;
}
.tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.3rem;
    align-items: center;
}
.difficulty-tag {
    color: var(--primary-color);
    border-radius: 8px;
    padding: 0.13rem 0.7rem;
    font-size: 0.85rem;
    font-weight: 600;
    margin-right: 0.3rem;
    text-transform: lowercase;
    border: 1px solid rgba(100,255,218,0.18);
}
.difficulty-tag.easy {
    color: #64ffda;
}
.difficulty-tag.medium {
    color: #ffd166;
}
.difficulty-tag.hard {
    color: #ff4e4e;
}
.tag {
    background: rgba(100,255,218,0.12);
    color: var(--primary-color);
    padding: 0.13rem 0.7rem;
    border-radius: var(--border-radius-sm);
    font-size: 0.82rem;
    font-weight: 500;
    border: 1px solid rgba(100,255,218,0.18);
}
.bets-pill {
    background: rgba(100,255,218,0.15);
    color: var(--primary-color);
    border-radius: 12px;
    padding: 0.13rem 0.8rem;
    font-size: 0.88rem;
    font-weight: 600;
    border: 1px solid rgba(100,255,218,0.18);
    margin-left: 0.5rem;
    white-space: nowrap;
}
.game-side {
    display: flex;
    flex-direction: column;
    align-items: flex-end;
    min-width: 120px;
    justify-content: center;
}
.side-row {
    display: flex;
    flex-direction: row;
    align-items: center;
    gap: 0.7rem;
}
.pnl {
    text-align: center;
    padding: 0.2rem 0.7rem;
    border-radius: 6px;
    background: rgba(100,255,218,0.07);
    min-width: 60px;
    margin-bottom: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    white-space: nowrap;
}
.pnl-label {
    display: block;
    font-size: 0.7rem;
    color: var(--secondary-color);
    margin-bottom: 0.1rem;
}
.pnl-value {
    font-size: 1.05rem;
    font-weight: 700;
}
.pnl.positive .pnl-value {
    color: #00ff88;
}
.pnl.negative .pnl-value {
    color: #ff4444;
}
.play-button {
    display: flex;
    align-items: center;
    justify-content: center;
    background: var(--primary-color);
    color: var(--background-dark);
    border-radius: 50%;
    width: 2.3rem;
    height: 2.3rem;
    font-size: 1.3rem;
    border: none;
    box-shadow: 0 2px 8px rgba(100,255,218,0.12);
    transition: background var(--transition-fast), color var(--transition-fast), box-shadow var(--transition-fast);
}
.play-button:hover {
    background: var(--secondary-color);
    color: var(--background-dark);
    box-shadow: 0 4px 16px rgba(100,255,218,0.18);
}
.play-button i {
    margin: 0;
}
</style>
