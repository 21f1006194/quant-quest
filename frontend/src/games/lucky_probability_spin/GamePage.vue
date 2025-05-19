<template>
  <div class="p-4 max-w-xl mx-auto">
    <h2 class="text-xl font-bold mb-4">🎰 Lucky Probability Spin</h2>
    
    <div class="mb-4">
      <label class="block font-semibold mb-1">Choose a color:</label>
      <select v-model="selectedColor" class="p-2 border rounded w-full">
        <option v-for="color in colors" :key="color" :value="color">{{ color }}</option>
      </select>
    </div>

    <button
      class="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
      @click="spin"
      :disabled="loading"
    >
      {{ loading ? "Spinning..." : "Spin the Wheel" }}
    </button>

    <div v-if="result" class="mt-6 p-4 border rounded shadow bg-white">
      <p><strong>Wheel landed on:</strong> {{ result.result }}</p>
      <p><strong>You {{ result.won ? "won" : "lost" }}!</strong></p>
      <p><strong>Payout:</strong> {{ result.payout }}</p>
      <p><strong>Expected Value:</strong> {{ result.expected_value }}</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import axios from "axios";

const selectedColor = ref("Red");
const colors = ["Red", "Blue", "Green", "Yellow", "Purple"];
const result = ref(null);
const loading = ref(false);

const spin = async () => {
  loading.value = true;
  try {
    const response = await axios.post("/api/lucky_spin/", {
      choice: selectedColor.value,
    });
    result.value = response.data;
  } catch (error) {
    alert("Error spinning wheel.");
  } finally {
    loading.value = false;
  }
};
</script>

<style scoped>
select {
  background-color: #f9fafb;
}
</style>
