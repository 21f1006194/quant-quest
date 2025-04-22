import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('access_token') || null,
        user: JSON.parse(localStorage.getItem('user')) || null,
    }),

    actions: {
        login(response) {
            const { access_token, user } = response;
            this.token = access_token;
            this.user = user;
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('user', JSON.stringify(user));
        },

        logout() {
            this.token = null;
            this.user = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
        },

        checkAuth() {
            return !!this.token;
        },
    },

    getters: {
        isAuthenticated() {
            return this.token !== null;
        },

        isAdmin() {
            return this.user?.is_admin === true;
        },

        isUser() {
            return this.user?.is_admin === false;
        },
    },
});
