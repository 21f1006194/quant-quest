import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('token') || null,
        user: null,
    }),

    actions: {
        login(token, user) {
            this.token = token;
            this.user = user;
            localStorage.setItem('token', token);
        },

        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('token');
        },

        checkAuth() {
            return !!this.token;
        },
    },

    getters: {
        isAuthenticated() {
            return this.token !== null;
        },
    },
});
