<template>
    <div class="game-toggle">
        <label :for="`game-toggle-${gameId}`">{{ gameName }}</label>
        <input :id="`game-toggle-${gameId}`" type="checkbox" :checked="isActive" @change="toggleGame" />
    </div>
</template>

<script>
export default {
    name: "GameToggle",
    props: {
        gameId: {
            type: Number,
            required: true,
        },
        gameName: {
            type: String,
            required: true,
        },
        isActive: {
            type: Boolean,
            required: true,
        },
    },
    methods: {
        toggleGame(event) {
            const newStatus = event.target.checked;
            this.$emit("toggle", { gameId: this.gameId, isActive: newStatus });
        },
    },
};
</script>

<style scoped>
.game-toggle {
    display: flex;
    align-items: center;
    margin: 10px 0;
}

label {
    margin-right: 10px;
}
</style>
