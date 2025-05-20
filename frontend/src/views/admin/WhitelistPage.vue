<template>
    <div class="whitelist-page">
        <div class="page-header">
            <h1>Whitelist Management</h1>
            <div class="header-buttons">
                <button class="whitelist-btn" @click="openWhitelistModal">
                    <i class="bi bi-person-plus"></i> Add User
                </button>
                <button class="bulk-upload-btn" @click="openBulkUploadModal">
                    <i class="bi bi-upload"></i> Bulk Upload
                </button>
            </div>
        </div>

        <!-- Summary Section -->
        <div class="summary-section">
            <div class="summary-card">
                <h3>Whitelist Overview</h3>
                <div class="overview-stats">
                    <div class="stat-item">
                        <span class="stat-label">Total Users</span>
                        <span class="stat-value">{{ whitelistedUsers.length }}</span>
                    </div>
                    <div class="stat-item">
                        <span class="stat-label">Physical Presence</span>
                        <span class="stat-value">{{ physicalCount }}</span>
                        <span class="stat-subtext">({{ Math.round((physicalCount / whitelistedUsers.length) * 100) || 0 }}%)</span>
                    </div>
                </div>
            </div>
            <div class="summary-card">
                <h3>Level Distribution</h3>
                <div class="level-distribution">
                    <div class="level-item">
                        <span class="level-label">Foundation</span>
                        <span class="level-value">{{ levelCounts.foundation }}</span>
                    </div>
                    <div class="level-item">
                        <span class="level-label">Diploma</span>
                        <span class="level-value">{{ levelCounts.diploma }}</span>
                    </div>
                    <div class="level-item">
                        <span class="level-label">Degree</span>
                        <span class="level-value">{{ levelCounts.degree }}</span>
                    </div>
                </div>
            </div>
        </div>

        <div class="search-sort-container">
            <div class="search-box">
                <i class="bi bi-search"></i>
                <input 
                    type="text" 
                    v-model="searchQuery" 
                    placeholder="Search by name or email..."
                    @input="handleSearch"
                >
            </div>
        </div>

        <div class="whitelist-grid">
            <div v-for="user in paginatedUsers" :key="user.email" class="whitelist-card">
                <div class="user-info">
                    <h2 class="user-name">{{ user.name }}</h2>
                    <div class="user-details">
                        <p class="email">
                            <i class="bi bi-envelope"></i>
                            {{ user.email }}
                        </p>
                        <p class="level">
                            <i class="bi bi-trophy"></i>
                            {{ user.level }}
                        </p>
                        <p class="physical-presence">
                            <i class="bi bi-geo-alt"></i>
                            {{ user.physical_presence ? 'Physical' : 'Virtual' }}
                        </p>
                    </div>
                </div>
                <div class="action-buttons">
                    <button class="delete-btn" @click="deleteUser(user.id)">
                        <i class="bi bi-trash"></i>
                    </button>
                </div>
            </div>
        </div>

        <div class="pagination">
            <button 
                :disabled="currentPage === 1" 
                @click="currentPage--"
                class="pagination-btn"
            >
                <i class="bi bi-chevron-left"></i>
            </button>
            <span class="page-info">Page {{ currentPage }} of {{ totalPages }}</span>
            <button 
                :disabled="currentPage === totalPages" 
                @click="currentPage++"
                class="pagination-btn"
            >
                <i class="bi bi-chevron-right"></i>
            </button>
        </div>

        <!-- Add User Modal -->
        <WhitelistUserModal
            :show="showWhitelistModal"
            @close="showWhitelistModal = false"
            @submitted="handleWhitelistSubmitted"
        />

        <!-- Bulk Upload Modal -->
        <div v-if="showBulkUploadModal" class="modal-overlay">
            <div class="modal-content">
                <div class="modal-header">
                    <h2>Bulk Upload Users</h2>
                    <button class="close-btn" @click="showBulkUploadModal = false">
                        <i class="bi bi-x"></i>
                    </button>
                </div>
                <div class="modal-body">
                    <div class="upload-area" 
                         @dragover.prevent 
                         @drop.prevent="handleFileDrop"
                         :class="{ 'dragging': isDragging }">
                        <input 
                            type="file" 
                            ref="fileInput" 
                            accept=".csv"
                            @change="handleFileSelect"
                            style="display: none"
                        >
                        <div class="upload-content">
                            <i class="bi bi-cloud-upload"></i>
                            <p>Drag and drop your CSV file here or</p>
                            <button class="upload-btn" @click="$refs.fileInput.click()">
                                Choose File
                            </button>
                            <p class="file-name" v-if="selectedFile">
                                Selected: {{ selectedFile.name }}
                            </p>
                        </div>
                    </div>
                    <div class="upload-instructions">
                        <h3>CSV Format Requirements:</h3>
                        <ul>
                            <li>Required columns: Name, Email, Level</li>
                            <li>Optional column: Any column containing "physical" for physical presence</li>
                            <li>First row should be headers</li>
                        </ul>
                    </div>
                </div>
                <div class="modal-footer">
                    <button class="cancel-btn" @click="showBulkUploadModal = false">Cancel</button>
                    <button 
                        class="upload-submit-btn" 
                        @click="handleBulkUpload"
                        :disabled="!selectedFile"
                    >
                        Upload
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/services/api';
import WhitelistUserModal from '@/components/modals/whiteListUSerModal.vue';

const whitelistedUsers = ref([]);
const filteredUsers = ref([]);
const searchQuery = ref('');
const showWhitelistModal = ref(false);
const showBulkUploadModal = ref(false);
const selectedFile = ref(null);
const isDragging = ref(false);
const currentPage = ref(1);
const itemsPerPage = 5;

// Computed properties for summary
const physicalCount = computed(() => {
    return whitelistedUsers.value.filter(user => user.physical_presence).length;
});

const levelCounts = computed(() => {
    const counts = {
        foundation: 0,
        diploma: 0,
        degree: 0
    };
    
    whitelistedUsers.value.forEach(user => {
        const level = user.level;
        if (level.startsWith('B')) {
            counts.degree++;
        } else if (level.toLowerCase().includes('diploma')) {
            counts.diploma++;
        } else {
            counts.foundation++;
        }
    });
    
    return counts;
});

// Pagination computed properties
const totalPages = computed(() => Math.ceil(filteredUsers.value.length / itemsPerPage));

const paginatedUsers = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return filteredUsers.value.slice(start, end);
});

const handleSearch = () => {
    currentPage.value = 1; // Reset to first page on search
    if (!searchQuery.value.trim()) {
        filteredUsers.value = [...whitelistedUsers.value];
    } else {
        const query = searchQuery.value.toLowerCase();
        filteredUsers.value = whitelistedUsers.value.filter(user => 
            user.name.toLowerCase().includes(query) ||
            user.email.toLowerCase().includes(query)
        );
    }
};

const fetchWhitelistedUsers = async () => {
    try {
        const response = await api.get('/admin/whitelist');
        whitelistedUsers.value = response.data.whitelisted_users;
        filteredUsers.value = [...whitelistedUsers.value];
    } catch (error) {
        console.error('Error fetching whitelisted users:', error);
    }
};

const openWhitelistModal = () => {
    showWhitelistModal.value = true;
};

const openBulkUploadModal = () => {
    showBulkUploadModal.value = true;
};

const handleWhitelistSubmitted = async () => {
    showWhitelistModal.value = false;
    await fetchWhitelistedUsers();
};

const deleteUser = async (id) => {
    if (!confirm('Are you sure you want to delete this user?')) return;
    
    try {
        await api.delete(`/admin/whitelist/${id}`);
        await fetchWhitelistedUsers();
    } catch (error) {
        console.error('Error deleting user:', error);
        alert('Error deleting user. Please try again.');
    }
};

const handleFileSelect = (event) => {
    const file = event.target.files[0];
    if (file && file.type === 'text/csv') {
        selectedFile.value = file;
    } else {
        alert('Please select a valid CSV file');
    }
};

const handleFileDrop = (event) => {
    isDragging.value = false;
    const file = event.dataTransfer.files[0];
    if (file && file.type === 'text/csv') {
        selectedFile.value = file;
    } else {
        alert('Please drop a valid CSV file');
    }
};

const handleBulkUpload = async () => {
    if (!selectedFile.value) return;

    const formData = new FormData();
    formData.append('file', selectedFile.value);

    try {
        await api.post('/admin/whitelist/bulk', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });
        showBulkUploadModal.value = false;
        selectedFile.value = null;
        await fetchWhitelistedUsers();
    } catch (error) {
        console.error('Error uploading file:', error);
        alert('Error uploading file. Please check the format and try again.');
    }
};

onMounted(() => {
    fetchWhitelistedUsers();
});
</script>

<style scoped>
.whitelist-page {
    padding: 1.5rem;
    max-width: 1200px;
    margin: 0 auto;
}

.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 1.5rem;
}

.page-header h1 {
    font-size: 1.75rem;
    color: #2c3e50;
    margin: 0;
}

.header-buttons {
    display: flex;
    gap: 1rem;
}

.whitelist-btn, .bulk-upload-btn {
    padding: 0.5rem 1rem;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: background-color 0.3s;
}

.whitelist-btn {
    background-color: #2196F3;
    color: white;
}

.bulk-upload-btn {
    background-color: #4CAF50;
    color: white;
}

.whitelist-btn:hover {
    background-color: #1976D2;
}

.bulk-upload-btn:hover {
    background-color: #45a049;
}

.whitelist-grid {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.whitelist-card {
    background: white;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: transform 0.2s;
}

.whitelist-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.user-info {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 2rem;
}

.user-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
    min-width: 200px;
}

.user-details {
    display: flex;
    align-items: center;
    gap: 2rem;
    flex: 1;
}

.user-details p {
    margin: 0;
    color: #666;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
}

.delete-btn {
    padding: 0.4rem;
    border: none;
    border-radius: 4px;
    background-color: #f44336;
    color: white;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
}

.delete-btn:hover {
    background-color: #da190b;
}

/* Modal Styles */
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
    max-width: 600px;
    max-height: 90vh;
    overflow-y: auto;
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
}

.modal-body {
    padding: 1rem;
}

.upload-area {
    border: 2px dashed #ccc;
    border-radius: 8px;
    padding: 2rem;
    text-align: center;
    margin-bottom: 1rem;
    transition: all 0.3s;
}

.upload-area.dragging {
    border-color: #4CAF50;
    background-color: rgba(76, 175, 80, 0.1);
}

.upload-content {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 1rem;
}

.upload-content i {
    font-size: 3rem;
    color: #666;
}

.upload-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
}

.file-name {
    margin-top: 0.5rem;
    color: #666;
    font-size: 0.9rem;
}

.upload-instructions {
    margin-top: 1rem;
    padding: 1rem;
    background-color: #f8f9fa;
    border-radius: 4px;
}

.upload-instructions h3 {
    margin: 0 0 0.5rem 0;
    font-size: 1rem;
    color: #2c3e50;
}

.upload-instructions ul {
    margin: 0;
    padding-left: 1.5rem;
    color: #666;
}

.modal-footer {
    padding: 1rem;
    border-top: 1px solid #eee;
    display: flex;
    justify-content: flex-end;
    gap: 1rem;
}

.cancel-btn, .upload-submit-btn {
    padding: 0.5rem 1rem;
    border-radius: 4px;
    cursor: pointer;
    font-weight: 600;
}

.cancel-btn {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    color: #666;
}

.upload-submit-btn {
    background-color: #4CAF50;
    border: none;
    color: white;
}

.upload-submit-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.summary-section {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 1rem;
    margin-bottom: 1.5rem;
}

.summary-card {
    background: white;
    border-radius: 8px;
    padding: 1rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.summary-card h3 {
    margin: 0 0 0.75rem 0;
    font-size: 1rem;
    color: #2c3e50;
    font-weight: 600;
}

.overview-stats {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 1rem;
}

.stat-item {
    display: flex;
    flex-direction: column;
    gap: 0.25rem;
    flex: 1;
}

.stat-label {
    font-size: 0.85rem;
    color: #666;
}

.stat-value {
    font-size: 1.5rem;
    font-weight: 600;
    color: #2c3e50;
}

.stat-subtext {
    font-size: 0.8rem;
    color: #666;
}

.level-distribution {
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
}

.level-item {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 0.25rem;
    flex: 1;
}

.level-label {
    color: #666;
    font-size: 0.85rem;
}

.level-value {
    font-weight: 600;
    color: #2c3e50;
    font-size: 1.25rem;
}

.search-sort-container {
    display: flex;
    gap: 1rem;
    margin-bottom: 1.5rem;
    width: 70%;
    align-items: center;
}

.search-box {
    flex: 1;
    position: relative;
    display: flex;
    align-items: center;
}

.search-box i {
    position: absolute;
    left: 1rem;
    color: #666;
}

.search-box input {
    width: 100%;
    padding: 0.5rem 1rem 0.5rem 2.5rem;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    font-size: 0.9rem;
    transition: border-color 0.3s;
}

.search-box input:focus {
    outline: none;
    border-color: #4CAF50;
}

.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 1rem;
    margin-top: 1.5rem;
}

.pagination-btn {
    background-color: #f8f9fa;
    border: 1px solid #dee2e6;
    padding: 0.4rem 0.75rem;
    border-radius: 4px;
    cursor: pointer;
    transition: all 0.3s;
}

.pagination-btn:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination-btn:not(:disabled):hover {
    background-color: #e9ecef;
}

.page-info {
    font-size: 0.9rem;
    color: #666;
}

@media (max-width: 768px) {
    .whitelist-card {
        flex-direction: column;
        align-items: flex-start;
        gap: 1rem;
    }

    .user-info {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .user-details {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .action-buttons {
        width: 100%;
        display: flex;
        justify-content: flex-end;
    }

    .summary-section {
        grid-template-columns: 1fr;
    }

    .search-sort-container {
        width: 100%;
    }

    .summary-section {
        grid-template-columns: 1fr;
    }

    .overview-stats {
        flex-direction: column;
        gap: 0.5rem;
    }

    .level-distribution {
        flex-direction: column;
        gap: 0.5rem;
    }

    .level-item {
        flex-direction: row;
        justify-content: space-between;
        padding: 0.25rem 0;
    }
}
</style> 