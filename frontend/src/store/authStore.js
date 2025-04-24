import { defineStore } from 'pinia';

export const useAuthStore = defineStore('auth', {
    state: () => ({
        token: localStorage.getItem('access_token') || null,
        user: JSON.parse(localStorage.getItem('user')) || null,
        api_token: localStorage.getItem('api_token') || null,
    }),

    actions: {
        login(response) {
            const { access_token, api_token, user } = response;
            this.token = access_token;
            this.user = user;
            this.api_token = api_token;
            localStorage.setItem('access_token', access_token);
            localStorage.setItem('user', JSON.stringify(user));
            if (api_token) {
                localStorage.setItem('api_token', api_token);
            }
        },

        logout() {
            this.token = null;
            this.user = null;
            this.api_token = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            localStorage.removeItem('api_token');
        },

        checkAuth() {
            return !!this.token;
        },

        resetApiToken(new_api_token) {
            this.api_token = new_api_token;
            localStorage.setItem('api_token', new_api_token);
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

        getApiToken() {
            if (this.api_token) {
                return this.api_token;
            }
            return null;
        },

    },
});
