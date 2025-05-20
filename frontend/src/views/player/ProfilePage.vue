<template>
    <div class="profile-container">
        <div class="profile-header">
            <h1>Profile Settings</h1>
        </div>

        <div class="profile-content">
            <!-- Profile Picture Section -->
            <div class="profile-section card profile-picture-section">
                <div class="profile-picture-container">
                    <div class="profile-picture-wrapper">
                        <img :src="avatarUrl || 'https://avatar.iran.liara.run/public'" alt="Profile Picture" class="profile-picture" />
                        <div class="profile-picture-overlay" @click="triggerFileInput">
                            <i class="bi bi-camera"></i>
                            <span>Change Photo</span>
                        </div>
                    </div>
                    <input 
                        type="file" 
                        ref="fileInput" 
                        @change="handleFileChange" 
                        accept="image/*" 
                        class="file-input" 
                        style="display: none"
                    />
                </div>
            </div>

            <!-- Personal Information Section -->
            <div class="profile-section card">
                <h2>Personal Information</h2>
                <div class="form-grid">
                    <div class="form-group">
                        <label>Display Name</label>
                        <input type="text" v-model="displayName" placeholder="Enter your full name" />
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" v-model="email" readonly />
                    </div>
                    <div class="form-group">
                        <label>Username</label>
                        <input type="text" v-model="username" readonly />
                    </div>
                    <div class="form-group full-width">
                        <label>Bio</label>
                        <textarea v-model="bio" placeholder="Tell us about yourself" rows="4"></textarea>
                    </div>
                </div>
                <button class="btn btn-primary" @click="saveProfile">
                    <i class="bi bi-save"></i> Save Changes
                </button>
            </div>

            <!-- API Keys Section -->
            <div class="profile-section card">
                <h2>API Keys</h2>
                <div class="api-keys-container">
                    <div class="api-key-item">
                        <label>API Key</label>
                        <div class="api-key-display">
                            <input type="password" v-model="apiKey" readonly />
                            <div class="api-key-actions">
                                <button class="icon-btn" @click="copyApiKey" title="Copy API Key">
                                    <i class="bi bi-clipboard"></i>
                                </button>
                                <button class="icon-btn" @click="regenerateApiKey" title="Regenerate API Key">
                                    <i class="bi bi-arrow-clockwise"></i>
                                </button>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/services/api';
import { useNotificationStore } from '@/store/notificationStore';

const notification = useNotificationStore();
const fileInput = ref(null);

// Profile data
const apiKey = ref('');
const displayName = ref('');
const email = ref('');
const username = ref('');
const bio = ref('');
const avatarUrl = ref('');

// Fetch profile data
const fetchProfile = async () => {
    try {
        const response = await api.get('/profile');
        if (response.status === 200) {
            const { profile } = response.data;
            displayName.value = profile.display_name || '';
            email.value = profile.email || '';
            username.value = profile.username || '';
            bio.value = profile.bio || '';
            apiKey.value = profile.api_key || '';
            avatarUrl.value = profile.avatar_url || '';
        }
    } catch (error) {
        notification.show('Failed to load profile data', 'red');
    }
};

// Save profile changes
const saveProfile = async () => {
    try {
        const response = await api.post('/profile', {
            display_name: displayName.value,
            bio: bio.value
        });
        if (response.status === 200) {
            notification.show('Profile updated successfully', 'green');
        }
    } catch (error) {
        notification.show('Failed to update profile', 'red');
    }
};

// Handle file selection
const triggerFileInput = () => {
    fileInput.value.click();
};

const handleFileChange = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Here you would typically upload the file to your server
    // For now, we'll just show a notification
    notification.show('Profile picture upload will be implemented soon', 'yellow');
};

// Copy API key to clipboard
const copyApiKey = () => {
    navigator.clipboard.writeText(apiKey.value);
    notification.show('API key copied to clipboard', 'green');
};

// Regenerate API key
const regenerateApiKey = async () => {
    if (!confirm('Are you sure you want to regenerate your API key? This will invalidate your current key.')) {
        return;
    }
    try {
        const response = await api.post('/profile/regenerate-key');
        if (response.status === 200) {
            apiKey.value = response.data.api_key;
            notification.show('API key regenerated successfully', 'green');
        }
    } catch (error) {
        notification.show('Failed to regenerate API key', 'red');
    }
};

onMounted(() => {
    fetchProfile();
});
</script>

<style scoped>
.profile-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: var(--spacing-lg);
}

.profile-header {
    margin-bottom: var(--spacing-xl);
}

.profile-header h1 {
    color: var(--primary-color);
    font-size: 2.5rem;
    text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
}

.profile-content {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-lg);
}

.profile-section {
    background-color: var(--card-dark);
    padding: var(--spacing-lg);
    border-radius: var(--border-radius-md);
    box-shadow: var(--shadow-md);
}

.profile-section h2 {
    color: var(--primary-color);
    margin-bottom: var(--spacing-md);
    font-size: 1.5rem;
}

/* Profile Picture Styles */
.profile-picture-section {
    display: flex;
    justify-content: center;
    padding: var(--spacing-xl);
}

.profile-picture-container {
    position: relative;
}

.profile-picture-wrapper {
    position: relative;
    width: 200px;
    height: 200px;
    border-radius: 50%;
    overflow: hidden;
    cursor: pointer;
}

.profile-picture {
    width: 100%;
    height: 100%;
    object-fit: cover;
}

.profile-picture-overlay {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
    opacity: 0;
    transition: opacity var(--transition-normal);
    color: white;
}

.profile-picture-wrapper:hover .profile-picture-overlay {
    opacity: 1;
}

.profile-picture-overlay i {
    font-size: 2rem;
    margin-bottom: var(--spacing-xs);
}

/* Form Styles */
.form-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: var(--spacing-md);
}

.form-group {
    margin-bottom: var(--spacing-md);
}

.form-group.full-width {
    grid-column: 1 / -1;
}

.form-group label {
    display: block;
    margin-bottom: var(--spacing-xs);
    color: var(--secondary-color);
}

.form-group input,
.form-group textarea {
    width: 100%;
    padding: var(--spacing-sm);
    background-color: var(--background-dark);
    border: 1px solid var(--secondary-color);
    border-radius: var(--border-radius-sm);
    color: var(--text-light);
    transition: border-color var(--transition-normal);
}

.form-group input:focus,
.form-group textarea:focus {
    outline: none;
    border-color: var(--primary-color);
}

.form-group input[readonly] {
    background-color: rgba(168, 178, 209, 0.1);
    cursor: not-allowed;
}

/* API Key Styles */
.api-keys-container {
    display: flex;
    flex-direction: column;
    gap: var(--spacing-md);
}

.api-key-item {
    margin-bottom: var(--spacing-sm);
}

.api-key-display {
    display: flex;
    gap: var(--spacing-sm);
    align-items: center;
}

.api-key-display input {
    flex: 1;
}

.api-key-actions {
    display: flex;
    gap: var(--spacing-xs);
}

.icon-btn {
    background: none;
    border: none;
    color: var(--primary-color);
    font-size: 1.2rem;
    padding: var(--spacing-xs);
    cursor: pointer;
    transition: color var(--transition-normal);
    border-radius: var(--border-radius-sm);
}

.icon-btn:hover {
    color: var(--secondary-color);
    background-color: rgba(100, 255, 218, 0.1);
}

.btn {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-xs);
    padding: var(--spacing-sm) var(--spacing-md);
    border: none;
    border-radius: var(--border-radius-sm);
    cursor: pointer;
    transition: all var(--transition-normal);
    font-weight: 500;
}

.btn-primary {
    background-color: var(--primary-color);
    color: var(--background-dark);
}

.btn-primary:hover {
    background-color: var(--secondary-color);
}

.btn i {
    font-size: 1.1em;
}

@media (max-width: 768px) {
    .profile-container {
        padding: var(--spacing-sm);
    }

    .profile-header h1 {
        font-size: 2rem;
    }

    .form-grid {
        grid-template-columns: 1fr;
    }

    .profile-picture-wrapper {
        width: 150px;
        height: 150px;
    }

    .api-key-display {
        flex-direction: column;
    }

    .api-key-actions {
        width: 100%;
        justify-content: center;
    }

    .btn {
        width: 100%;
        justify-content: center;
    }
}
</style>