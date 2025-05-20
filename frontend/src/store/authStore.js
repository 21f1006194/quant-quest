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
            localStorage.setItem('avatar_url', user.avatar_url);
            localStorage.setItem('full_name', user.full_name);
        },

        logout() {
            this.token = null;
            this.user = null;
            this.api_token = null;
            localStorage.removeItem('access_token');
            localStorage.removeItem('user');
            localStorage.removeItem('api_token');
            localStorage.removeItem('avatar_url');
            localStorage.removeItem('full_name');
        },

        checkAuth() {
            return !!this.token;
        },

        resetApiToken(new_api_token) {
            this.api_token = new_api_token;
            localStorage.setItem('api_token', new_api_token);
        },

        resetUserInfo(new_user_info) {
            this.user = new_user_info;
            localStorage.setItem('user', JSON.stringify(new_user_info));
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
        getAvatarUrl() {
            if (this.user?.avatar_url) {
                return this.user.avatar_url;
            }
            return null;
        },
        getFullName() {
            if (this.user?.full_name) {
                return this.user.full_name;
            }
            return null;
        }

    },
});
