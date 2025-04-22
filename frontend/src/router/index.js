import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from '../store/authStore';

import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import LoginView from "../views/LoginView.vue";
import Register from '../views/Register.vue';
import AdminDash from '../views/admin/AdminDash.vue';
import PlayerDash from '../views/player/PlayerDash.vue';
import GameWrapper from '../views/GameWrapper.vue';

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
            path: "/player",
            name: 'Player',
            component: PlayerDash,
            meta: { requiresUser: true }
        },
        { path: "/", component: HomeView },
        { path: "/about", component: AboutView },
        { path: "/login", name: 'Login', component: LoginView },
        { path: '/register', name: 'Register', component: Register },
        {
            path: '/game/:gameName',
            component: GameWrapper,
            meta: { requiresUser: true },
            children: [
                {
                    path: '',
                    component: () => import('@/games/GameNotFound.vue'),
                    beforeEnter: (to) => {
                        const gameName = to.params.gameName;
                        return import(`@/games/${gameName}/GamePage.vue`)
                            .then(module => {
                                to.matched[0].components.default = module.default;
                            })
                            .catch(() => {
                                // Keep the default GameNotFound component
                            });
                    }
                }
            ]
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

    next();
});

export default router;
