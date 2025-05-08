<template>
  <div v-if="show" class="modal">
    <div class="modal-content">
      <span class="close" @click="closeModal">&times;</span>
      <h2>
        {{ isBulk ? 'Bulk Bonus' : isBonus ? `Bonus for ${username}` : `Penalty for ${username}` }}
      </h2>
      <form @submit.prevent="submitForm">
        <div class="form-group">
          <label for="amount">Amount:</label>
          <input type="number" v-model="amount" required />
        </div>
        <div class="form-group">
          <label for="description">Description:</label>
          <textarea v-model="description" required></textarea>
        </div>
        <button type="submit">Submit</button>
        <button type="button" class="close-button" @click="closeModal">Close</button>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';

const props = defineProps({
  show: Boolean,
  userId: Number,
  username: String,
  isBonus: Boolean,
  isBulk: Boolean
});

const emit = defineEmits(['close', 'submitted']);

const amount = ref(0);
const description = ref('');

const closeModal = () => {
    amount.value = 0;
    description.value = '';
  emit('close');
};

const submitForm = async () => {
  try {
    if (amount.value <= 0) {
      alert('Amount must be greater than 0');
      return;
    }
    const endpoint = props.isBulk
      ? '/admin/bonus/to_all'
      : props.isBonus
      ? `/admin/bonus/${props.userId}`
      : `/admin/penalty/${props.userId}`;

    const response = await api.post(endpoint, {
      amount: amount.value,
      description: description.value
    });
    emit('submitted', response.data);
    closeModal();
  } catch (error) {
    console.error('Error submitting form:', error);
  }
};
</script>

<style scoped>
.modal {
  display: flex;
  justify-content: center;
  align-items: center;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.7);
}

.modal-content {
  background-color: #333;
  padding: 20px;
  border-radius: 5px;
  width: 400px;
  max-width: 90%;
  color: #fff;
}

.close {
  float: right;
  font-size: 24px;
  cursor: pointer;
}

.form-group {
  margin-bottom: 15px;
}

input, textarea {
  background-color: #f0f0f0;
  color: #333;
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px;
  width: 100%;
  box-sizing: border-box;
}

button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

.close-button {
  background-color: #f44336;
  color: white;
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  margin-top: 10px;
  margin-left: 10px;
}

.close-button:hover {
  background-color: #d32f2f;
}
</style>
