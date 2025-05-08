<template>
  <div class="player-dashboard">
    <div class="dashboard-header">
      <h1>Player Dashboard</h1>
    </div>
    <p>Welcome to your dashboard. Here you can view your stats and recent activities.</p>
    <div class="dashboard-cards">
      <div class="card">
        <h2>Your Games</h2>
        <p>{{ totalGames }}</p>
      </div>
      <div class="card">
        <h2>Your Achievements</h2>
        <p>{{ totalAchievements }}</p>
      </div>
      <div class="card">
        <h2>Recent Activities</h2>
        <ul>
          <li v-for="activity in recentActivities" :key="activity.id">{{ activity.description }}</li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.wallet-card {
  background-color: #343434;
  padding: 15px 25px;
  border-radius: 10px;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 5px;
  min-width: 200px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  border: 1px solid #484848;
}

.wallet-card i {
  color: #00ff00;
  font-size: 1.2em;
  margin-right: 8px;
}

.wallet-card span {
  font-size: 1.5em;
  font-weight: bold;
  color: #fff;
  display: flex;
  align-items: center;
}

.wallet-timestamp {
  color: #888;
  font-size: 0.8em;
}

.player-dashboard {
  padding: 20px;
}

.dashboard-cards {
  display: flex;
  gap: 20px;
}

.card {
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 5px;
  flex: 1;
}
</style>
