import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
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
        { path: "/login", name: 'Login', component: LoginView },
        { path: '/register', name: 'Register', component: Register }

    ],


});


export default router;
