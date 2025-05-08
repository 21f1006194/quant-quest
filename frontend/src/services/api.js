import axios from "axios";
import { useAuthStore } from '@/store/authStore';

const api = axios.create({
    baseURL: "http://localhost:5000",
});

// add token to headers
api.interceptors.request.use((config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
        config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});

// unauthorized error handler
api.interceptors.response.use(
    (response) => response,
    (error) => {
        // Handle authentication errors (401)
        // 401: Unauthorized - Authentication is required or has failed
        // 403: Forbidden - User is authenticated but doesn't have permission
        // 422: Unprocessable Entity - Validation errors or semantic issues
        alert(`Error: ${error.response?.status} ${error.response?.data?.error}`);
        const errorMessage = error.response?.data?.error.toLowerCase();
        if (error.response?.status === 401
            || errorMessage.includes('signature') && errorMessage.includes('failed')
            || errorMessage.includes('token') && errorMessage.includes('expired')
            || errorMessage.includes('token') && errorMessage.includes('invalid')
        ) {
            const authStore = useAuthStore();
            authStore.logout();
            window.location.href = "/login";
        }
        return Promise.reject(error);
    }
);

export default api;
