import { createRouter, createWebHistory } from "vue-router";

import HomeView from "../views/HomeView.vue";
import LoginView from "../views/LoginView.vue";
import Register from '../views/Register.vue';

const router = createRouter({
    history: createWebHistory(),
    routes: [
        
        { path: "/", component:  HomeView},
        { path: "/Login", name: 'Login', component:  LoginView},
        { path: '/register', component: Register }
    ],


});


export default router;
