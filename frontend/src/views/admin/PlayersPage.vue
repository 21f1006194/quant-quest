<template>
    <div v-if="showSuccessMessage" class="success-message" style="position: fixed; top: 10px; right: 10px; background-color: #4CAF50; color: white; padding: 10px; border-radius: 5px; z-index: 1000;"> 
        <i class="bi bi-check-circle"></i>
        User whitelisted successfully
    </div>
    <div class="players-page">
        <div class="page-header">
            <h1>Players</h1>
            <div class="header-buttons">
                <button class="bulk-bonus-btn" @click="openBulkBonusModal">
                    <i class="bi bi-gift"></i> Bulk Bonus
                </button>
            </div>
        </div>

        <div class="search-sort-container">
            <div class="search-box">
                <i class="bi bi-search"></i>
                <input 
                    type="text" 
                    v-model="searchQuery" 
                    placeholder="Search by name, username or email..."
                    @input="handleSearch"
                >
            </div>
            <button 
                class="sort-btn" 
                @click="toggleSort"
                :class="{ 'active': sortDirection !== null }"
            >
                <i class="bi" :class="sortIcon"></i>
                Sort by Balance
            </button>
        </div>

        <div class="players-grid">
            <div v-for="player in paginatedPlayers" :key="player.id" class="player-card">
                <div class="player-info">
                    <h2 class="player-name">{{ player.full_name }}</h2>
                    <div class="player-details">
                        <p class="username">
                            <i class="bi bi-person"></i>
                            {{ player.username }}
                        </p>
                        <div class="wallet-info">
                            <p class="balance">
                                <i class="bi bi-wallet2"></i>
                                ${{ player.wallet_balance }}
                            </p>
                            <p class="last-updated">
                                <i class="bi bi-clock"></i>
                                {{ formatDate(player.wallet_last_updated) }}
                            </p>
                        </div>
                    </div>
                </div>
                <div class="action-buttons">
                    <button class="bonus-btn" @click="openModal(true, player.id, player.username)">
                        <i class="bi bi-plus-circle"></i>
                    </button>
                    <button class="penalty-btn" @click="openModal(false, player.id, player.username)">
                        <i class="bi bi-dash-circle"></i>
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

        <BonusPenalityModal
            :show="showBonusModal"
            :userId="selectedUserId"
            :username="selectedUsername"
            :isBonus="true"
            @close="showBonusModal = false"
            @submitted="handleSubmitted"
        />
        <BonusPenalityModal
            :show="showPenaltyModal"
            :userId="selectedUserId"
            :username="selectedUsername"
            :isBonus="false"
            @close="showPenaltyModal = false"
            @submitted="handleSubmitted"
        />
        <BonusPenalityModal
            :show="showBulkBonusModal"
            :isBulk="true"
            @close="showBulkBonusModal = false"
            @submitted="handleSubmitted"
        />
    </div>
</template>

<script setup>
import { ref, onMounted, computed } from "vue";
import api from "@/services/api";
import BonusPenalityModal from "@/components/modals/BonusPenalityModal.vue";

const players = ref([]);
const filteredPlayers = ref([]);
const searchQuery = ref('');
const sortDirection = ref(null); // null, 'asc', or 'desc'
const showBonusModal = ref(false);
const showPenaltyModal = ref(false);
const selectedUserId = ref(null);
const selectedUsername = ref('');
const showBulkBonusModal = ref(false);
const currentPage = ref(1);
const itemsPerPage = 5;
const showSuccessMessage = ref(false);

const sortIcon = computed(() => {
    if (sortDirection.value === 'asc') return 'bi-sort-up';
    if (sortDirection.value === 'desc') return 'bi-sort-down';
    return 'bi-sort';
});

const totalPages = computed(() => Math.ceil(filteredPlayers.value.length / itemsPerPage));

const paginatedPlayers = computed(() => {
    const start = (currentPage.value - 1) * itemsPerPage;
    const end = start + itemsPerPage;
    return filteredPlayers.value.slice(start, end);
});

const handleSearch = () => {
    currentPage.value = 1; // Reset to first page on search
    if (!searchQuery.value.trim()) {
        filteredPlayers.value = [...players.value];
    } else {
        const query = searchQuery.value.toLowerCase();
        filteredPlayers.value = players.value.filter(player => 
            player.full_name.toLowerCase().includes(query) ||
            player.username.toLowerCase().includes(query) ||
            player.email.toLowerCase().includes(query)
        );
    }
    applySort();
};

const toggleSort = () => {
    if (sortDirection.value === null) {
        sortDirection.value = 'desc';
    } else if (sortDirection.value === 'desc') {
        sortDirection.value = 'asc';
    } else {
        sortDirection.value = null;
    }
    applySort();
};

const applySort = () => {
    if (sortDirection.value === null) {
        // If no sort direction, maintain search results order
        return;
    }
    
    filteredPlayers.value.sort((a, b) => {
        const balanceA = parseFloat(a.wallet_balance);
        const balanceB = parseFloat(b.wallet_balance);
        return sortDirection.value === 'asc' 
            ? balanceA - balanceB 
            : balanceB - balanceA;
    });
};

const formatDate = (dateString) => {
    return new Date(dateString).toLocaleString();
};

const fetchPlayers = async () => {
    const response = await api.get("/admin/all_users");
    players.value = response.data.users;
    filteredPlayers.value = [...players.value];
};

const openModal = (isBonus, userId, username) => {
    if (isBonus) {
        showBonusModal.value = true;
    } else {
        showPenaltyModal.value = true;
    }
    selectedUserId.value = userId;
    selectedUsername.value = username;
};

const openBulkBonusModal = () => {
    showBulkBonusModal.value = true;
};

const handleSubmitted = (data) => {
    console.log('Form submitted:', data);
    fetchPlayers();
};

onMounted(() => {
    fetchPlayers();
});

</script>

<style scoped>
.players-page {
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

.bulk-bonus-btn {
    background-color: #4CAF50;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 6px;
    cursor: pointer;
    font-weight: 600;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: background-color 0.3s;
}

.bulk-bonus-btn:hover {
    background-color: #45a049;
}

.players-grid {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
}

.player-card {
    background: white;
    border-radius: 8px;
    padding: 0.75rem 2rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    transition: transform 0.2s;
    min-width: 800px;
}

.player-card:hover {
    transform: translateY(-1px);
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.15);
}

.player-info {
    flex: 1;
    display: flex;
    align-items: center;
    gap: 2rem;
}

.player-name {
    font-size: 1.1rem;
    font-weight: 600;
    color: #2c3e50;
    margin: 0;
    min-width: 200px;
}

.player-details {
    display: flex;
    align-items: center;
    gap: 2rem;
    flex: 1;
}

.username {
    margin: 0;
    color: #666;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
}

.wallet-info {
    display: flex;
    gap: 1.5rem;
    align-items: center;
}

.wallet-info p {
    margin: 0;
    color: #666;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    font-size: 0.9rem;
}

.action-buttons {
    display: flex;
    gap: 0.5rem;
}

.bonus-btn, .penalty-btn {
    padding: 0.4rem;
    border: none;
    border-radius: 4px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.3s;
    font-size: 1.1rem;
}

.bonus-btn {
    background-color: #4CAF50;
    color: white;
}

.penalty-btn {
    background-color: #f44336;
    color: white;
}

.bonus-btn:hover {
    background-color: #45a049;
}

.penalty-btn:hover {
    background-color: #da190b;
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

.sort-btn {
    padding: 0.5rem 0.75rem;
    border: 1px solid #dee2e6;
    border-radius: 6px;
    background: white;
    color: #666;
    cursor: pointer;
    display: flex;
    align-items: center;
    gap: 0.5rem;
    transition: all 0.3s;
    font-size: 0.9rem;
    min-width: 120px;
    justify-content: center;
    white-space: nowrap;
}

.sort-btn i {
    font-size: 1rem;
}

.sort-btn:hover {
    background: #f8f9fa;
    border-color: #4CAF50;
    color: #4CAF50;
}

.sort-btn.active {
    background: #4CAF50;
    color: white;
    border-color: #4CAF50;
}

.sort-btn.active:hover {
    background: #45a049;
    color: white;
}

@media (max-width: 900px) {
    .player-card {
        min-width: unset;
        width: 100%;
    }
    
    .player-info {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }
    
    .player-name {
        min-width: unset;
    }
    
    .player-details {
        flex-direction: column;
        align-items: flex-start;
        gap: 0.5rem;
    }

    .search-sort-container {
        width: 100%;
        flex-direction: row;
        align-items: center;
    }
    
    .search-box {
        width: 100%;
    }
    
    .sort-btn {
        min-width: 100px;
        padding: 0.5rem;
    }
}
</style>
