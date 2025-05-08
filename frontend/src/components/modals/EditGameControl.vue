<template>
  <div class="modal-overlay" v-if="show" @click.self="close">
    <div class="modal-content">
      <h2>Edit Game Settings</h2>
      
      <div class="form-section">
        <div class="form-header">
          <h3>Basic Settings</h3>
        </div>
        
        <div class="form-group">
          <label>Game Name</label>
          <input type="text" v-model="gameData.name" disabled class="disabled-input" />
        </div>

        <div class="form-row">
          <div class="form-group toggle-group">
            <div class="toggle-switch" :class="{ active: gameData.is_active }" @click="toggleActive">
              <div class="toggle-slider"></div>
            </div>
            <span class="toggle-label">{{ gameData.is_active ? 'Active' : 'Inactive' }}</span>
          </div>

          <div class="form-group">
            <label>Difficulty</label>
            <select v-model="gameData.difficulty">
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label>Max Sessions per User</label>
            <input type="number" v-model.number="gameData.max_sessions_per_user" min="1" />
          </div>

          <div class="form-group">
            <label>Max Bets per Session</label>
            <input type="number" v-model.number="gameData.max_bets_per_session" min="1" />
          </div>
        </div>

        <div class="form-group">
          <label>Tags</label>
          <input type="text" v-model="gameData.tags" placeholder="Comma-separated tags" />
        </div>
      </div>

      <div class="form-section">
        <div class="form-header">
          <h3>Configuration Data</h3>
        </div>
        <div class="form-group">
          <textarea
            v-model="configDataString"
            @input="validateJson"
            :class="{ 'error': jsonError }"
            placeholder="Enter JSON configuration"
            rows="8"
          ></textarea>
          <span class="error-message" v-if="jsonError">{{ jsonError }}</span>
        </div>
      </div>

      <div class="modal-actions">
        <button @click="saveChanges" class="save-btn" :disabled="!!jsonError">Save Changes</button>
        <button @click="close" class="cancel-btn">Cancel</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import api from '@/services/api'

const props = defineProps({
  show: Boolean,
  game: Object
})

const emit = defineEmits(['close', 'saved'])

const gameData = ref({
  name: '',
  is_active: false,
  max_sessions_per_user: 1,
  max_bets_per_session: 1,
  difficulty: 'medium',
  tags: '',
  config_data: {}
})

const jsonError = ref('')
const configDataString = computed({
  get: () => {
    try {
      return JSON.stringify(gameData.value.config_data, null, 2)
    } catch (e) {
      return '{}'
    }
  },
  set: (value) => {
    try {
      gameData.value.config_data = JSON.parse(value)
      jsonError.value = ''
    } catch (e) {
      jsonError.value = 'Invalid JSON format'
    }
  }
})

watch(() => props.game, (newGame) => {
  if (newGame) {
    gameData.value = { ...newGame }
    if (!gameData.value.config_data) {
      gameData.value.config_data = {}
    }
  }
}, { immediate: true })

const toggleActive = () => {
  gameData.value.is_active = !gameData.value.is_active
}

const validateJson = () => {
  try {
    JSON.parse(configDataString.value)
    jsonError.value = ''
  } catch (e) {
    jsonError.value = 'Invalid JSON format'
  }
}

const close = () => {
  emit('close')
}

const saveChanges = async () => {
  if (jsonError.value) return

  try {
    const encodedName = encodeURIComponent(gameData.value.name)
    const payload = {
      max_sessions_per_user: Number(gameData.value.max_sessions_per_user),
      max_bets_per_session: Number(gameData.value.max_bets_per_session),
      config_data: gameData.value.config_data,
      is_active: Boolean(gameData.value.is_active),
      difficulty: String(gameData.value.difficulty),
      tags: gameData.value.tags
    }

    console.log(payload)
    console.log(encodedName)
    await api.post(`/game/${encodedName}/control`, payload)
    emit('saved')
    close()
  } catch (error) {
    console.error('Error saving game settings:', error)
    alert('Failed to save game settings')
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: #2a2a2a;
  padding: 24px;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  color: white;
  max-height: 90vh;
  overflow-y: auto;
}

.form-section {
  margin-bottom: 24px;
  background-color: #343434;
  padding: 16px;
  border-radius: 6px;
}

.form-header {
  margin-bottom: 16px;
}

.form-header h3 {
  margin: 0;
  color: #ccc;
  font-size: 1.1em;
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #ccc;
}

.form-group input,
.form-group select,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #484848;
  border-radius: 4px;
  background-color: #2a2a2a;
  color: white;
  font-family: monospace;
}

.form-group textarea {
  resize: vertical;
  min-height: 120px;
}

.disabled-input {
  background-color: #1a1a1a !important;
  cursor: not-allowed;
}

.form-row {
  display: flex;
  gap: 16px;
  margin-bottom: 16px;
}

.form-row .form-group {
  flex: 1;
  margin-bottom: 0;
}

.toggle-group {
  display: flex;
  align-items: center;
  gap: 12px;
  padding-top: 24px;
}

.toggle-switch {
  position: relative;
  width: 50px;
  height: 24px;
  background-color: #666;
  border-radius: 12px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.toggle-switch.active {
  background-color: #4CAF50;
}

.toggle-slider {
  position: absolute;
  top: 2px;
  left: 2px;
  width: 20px;
  height: 20px;
  background-color: white;
  border-radius: 50%;
  transition: transform 0.3s;
}

.toggle-switch.active .toggle-slider {
  transform: translateX(26px);
}

.toggle-label {
  color: #ccc;
  font-size: 0.9em;
}

.error {
  border-color: #ff4444 !important;
}

.error-message {
  color: #ff4444;
  font-size: 0.9em;
  margin-top: 4px;
  display: block;
}

.modal-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 24px;
}

.save-btn,
.cancel-btn {
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  font-weight: 500;
}

.save-btn {
  background-color: #4CAF50;
  color: white;
}

.save-btn:disabled {
  background-color: #666;
  cursor: not-allowed;
}

.cancel-btn {
  background-color: #666;
  color: white;
}

.save-btn:hover:not(:disabled) {
  background-color: #45a049;
}

.cancel-btn:hover {
  background-color: #555;
}
</style>
