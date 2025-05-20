<template>
    <div v-if="show" class="modal-overlay">
        <div class="modal-content">
            <div class="modal-header">
                <h2>Whitelist User</h2>
                <button class="close-btn" @click="$emit('close')">
                    <i class="bi bi-x"></i>
                </button>
            </div>
            
            <form @submit.prevent="handleSubmit" class="modal-body">
                <div class="form-group">
                    <label for="email">Email *</label>
                    <input 
                        type="email" 
                        id="email" 
                        v-model="formData.email" 
                        required
                        placeholder="Enter user's email"
                    >
                </div>

                <div class="form-group">
                    <label for="name">Name</label>
                    <input 
                        type="text" 
                        id="name" 
                        v-model="formData.name" 
                        placeholder="Enter user's name"
                    >
                </div>

                <div class="form-group">
                    <label for="level">Level</label>
                    <select 
                        id="level" 
                        v-model="formData.level"
                    >
                        <option value="" disabled>Select level</option>
                        <option value="foundation">Foundation</option>
                        <option value="diploma">Diploma</option>
                        <option value="degree">Degree</option>
                    </select>
                </div>

                <div class="form-group checkbox">
                    <label>
                        <input 
                            type="checkbox" 
                            v-model="formData.physical_presence"
                        >
                        Physical Presence 
                    </label>
                </div>

                <div class="error-message" v-if="error">
                    {{ error }}
                </div>

                <div class="modal-footer">
                    <button type="button" class="cancel-btn" @click="$emit('close')">Cancel</button>
                    <button type="submit" class="submit-btn" :disabled="loading">
                        {{ loading ? 'Whitelisting...' : 'Whitelist User' }}
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import api from '@/services/api';

const props = defineProps({
    show: {
        type: Boolean,
        required: true
    }
});

const emit = defineEmits(['close', 'submitted']);

const formData = ref({
    email: '',
    name: '',
    level: '',
    physical_presence: false
});

const loading = ref(false);
const error = ref('');

const handleSubmit = async () => {
    try {
        loading.value = true;
        error.value = '';
        
        const response = await api.post('/admin/whitelist', formData.value);
        
        // Reset form
        formData.value = {
            email: '',
            name: '',
            level: '',
            physical_presence: false
        };
        
        emit('submitted', response.data);
        emit('close');
    } catch (err) {
        error.value = err.response?.data?.error || 'Failed to whitelist user';
    } finally {
        loading.value = false;
    }
};
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
    background: white;
    border-radius: 8px;
    width: 90%;
    max-width: 500px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.modal-header {
    padding: 1rem;
    border-bottom: 1px solid #eee;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.modal-header h2 {
    margin: 0;
    font-size: 1.25rem;
    color: #2c3e50;
}

.close-btn {
    background: none;
    border: none;
    font-size: 1.5rem;
    cursor: pointer;
    color: #666;
    padding: 0.25rem;
}

.modal-body {
    padding: 1.5rem;
}

.form-group {
    margin-bottom: 1rem;
}

.form-group label {
    display: block;
    margin-bottom: 0.5rem;
    color: #2c3e50;
    font-weight: 500;
}

.form-group input[type="text"],
.form-group input[type="email"],
.form-group input[type="number"] {
    width: 100%;
    padding: 0.5rem;
    border: 1px solid #ddd;
    border-radius: 4px;
    font-size: 0.9rem;
}

.form-group.checkbox {
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.form-group.checkbox label {
    margin: 0;
    font-weight: normal;
}

.error-message {
    color: #dc3545;
    margin-bottom: 1rem;
    font-size: 0.9rem;
}

.modal-footer {
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
    margin-top: 1.5rem;
}

.cancel-btn,
.submit-btn {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 500;
    transition: all 0.3s;
}

.cancel-btn {
    background: #f8f9fa;
    border: 1px solid #dee2e6;
    color: #666;
}

.submit-btn {
    background: #4CAF50;
    border: none;
    color: white;
}

.submit-btn:disabled {
    opacity: 0.7;
    cursor: not-allowed;
}

.cancel-btn:hover {
    background: #e9ecef;
}

.submit-btn:not(:disabled):hover {
    background: #45a049;
}
</style>
