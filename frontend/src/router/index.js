import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from '../store/authStore';
import { getGameinfo } from '@/services/gameService';
import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import LoginView from "../views/LoginView.vue";
import SecretLogin from '../views/SecretLogin.vue';
import AdminDash from '../views/admin/AdminDash.vue';
import PlayerDash from '../views/player/PlayerDash.vue';
import GameWrapper from '../views/GameWrapper.vue';
import PlayerGamesView from '../views/player/PlayerGamesView.vue';
import PlayersPage from '../views/admin/PlayersPage.vue';
import WhitelistPage from '../views/admin/WhitelistPage.vue';
const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: "/admin",
            name: 'Admin',
            component: AdminDash,
            meta: { requiresAdmin: true }
        },
        {
            path: "/admin/players",
            name: 'AdminPlayers',
            component: PlayersPage,
            meta: { requiresAdmin: true }
        },
        {
            path: "/admin/whitelist",
            name: 'AdminWhitelist',
            component: WhitelistPage,
            meta: { requiresAdmin: true }
        },
        {
            path: "/player",
            name: 'Player',
            component: PlayerDash,
            meta: { requiresUser: true }
        },
        {
            path: "/games",
            name: 'PlayerGames',
            component: PlayerGamesView,
            meta: { requiresUser: true }
        },
        { path: "/", component: HomeView },
        { path: "/about", component: AboutView },
        { path: "/login", name: 'Login', component: LoginView },
        { path: "/system/access", name: 'SecretLogin', component: SecretLogin },
        {
            path: '/game/:gameName',
            component: GameWrapper,
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    component: () => import('@/games/GameNotFound.vue'),
                    beforeEnter: async (to) => {
                        const gameName = to.params.gameName;
                        try {
                            // Fetch game info
                            const gameData = await getGameinfo(gameName);

                            // If game is not active, redirect to a not active page
                            if (!gameData.is_active) {
                                return { name: 'GameNotActive', params: { gameName } };
                            }

                            // Try to load the game component
                            const module = await import(`@/games/${gameName}/GamePage.vue`);
                            to.matched[0].components.default = module.default;

                            // Pass game data to the component
                            to.meta.gameData = gameData;
                        } catch (error) {
                            console.error('Error loading game:', error);
                            // Keep the default GameNotFound component
                        }
                    }
                }
            ]
        },
        {
            path: '/game/:gameName/docs',
            component: GameWrapper,
            meta: { requiresAuth: true },
            children: [
                {
                    path: '',
                    component: () => import('@/games/GameNotFound.vue'),
                    beforeEnter: async (to) => {
                        const gameName = to.params.gameName;
                        try {
                            const gameData = await getGameinfo(gameName);
                            if (!gameData.is_active) {
                                return { name: 'GameNotActive', params: { gameName } };
                            }
                            // Load the simple game page
                            const module = await import('@/games/SimpleGamePage.vue');
                            to.matched[0].components.default = module.default;
                            // Pass game data to the component
                            to.meta.gameData = gameData;
                        } catch (error) {
                            console.error('Error loading game:', error);
                        }
                    }
                }
            ]
        },
        {
            path: '/game/:gameName/not-active',
            name: 'GameNotActive',
            component: () => import('@/games/GameNotActive.vue'),
            meta: { requiresUser: true }
        }
    ],
});

// Navigation guard
router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();

    // Check if route requires admin access
    if (to.matched.some(record => record.meta.requiresAdmin)) {
        if (!authStore.isAdmin) {
            next({ name: 'Login' });
            return;
        }
    }

    // Check if route requires user access
    if (to.matched.some(record => record.meta.requiresUser)) {
        if (!authStore.isUser) {
            next({ name: 'Login' });
            return;
        }
    }

    // Check if route requires authentication
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!authStore.isAuthenticated) {
            next({ name: 'Login' });
            return;
        }
    }

    // If all checks pass, proceed with navigation
    next();
});

export default router;
