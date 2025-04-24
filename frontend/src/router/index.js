import { createRouter, createWebHistory } from "vue-router";
import { useAuthStore } from '@/store/authStore';

import HomeView from "../views/HomeView.vue";
import AboutView from "../views/AboutView.vue";
import LoginView from "../views/LoginView.vue";
import Register from '../views/Register.vue';
import AdminDash from '../views/admin/AdminDash.vue';
import PlayerDash from '../views/player/PlayerDash.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        { path: "/admin", name: 'Admin', component: AdminDash },
        { path: "/player", name: 'Player', component: PlayerDash },
        { path: "/", component: HomeView },
        { path: "/about", component: AboutView },
        { path: "/login", name: 'Login', component: LoginView },
        { path: '/register', name: 'Register', component: Register },
        {
            path: '/admin/games',
            name: 'AdminGames',
            component: () => import('@/views/admin/AdminDash.vue'),
            meta: { requiresAuth: true, isAdmin: true }
        }
    ],
});

router.beforeEach((to, from, next) => {
    const authStore = useAuthStore();
    const token = localStorage.getItem('token');

    // Check if the route requires authentication
    if (to.meta.requiresAuth) {
        if (!token) {
            // Redirect to login if no token is found
            return next({ path: '/login' });
        }

        // Check if the route requires admin privileges
        if (to.meta.isAdmin && !authStore.isAdmin) {
            // Redirect to login if the user is not an admin
            return next({ path: '/login' });
        }
    }

    next();
});

export default router;
