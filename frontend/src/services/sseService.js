import { useAuthStore } from '@/store/authStore';
import api from './api';

class SSEService {
    constructor() {
        this.connection = null;
        this.isConnected = false;
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.eventHandlers = new Map();
    }

    connect() {
        if (this.connection) {
            this.connection.close();
        }

        const authStore = useAuthStore();
        const token = authStore.token;
        if (!token) {
            console.error('No token available for SSE connection');
            return;
        }

        // Use URL parameters for authentication
        const baseUrl = api.defaults.baseURL.replace(/\/$/, '');
        const url = `${baseUrl}/sse?auth_token=${encodeURIComponent(token)}`;

        try {
            this.connection = new EventSource(url);
            console.log('EventSource created successfully');

            this.connection.onopen = () => {
                this.isConnected = true;
                this.reconnectAttempts = 0;
                console.log('SSE Connected successfully');
            };

            this.connection.onmessage = (event) => {
                try {
                    const data = JSON.parse(event.data);
                    console.log('SSE Message received:', data);
                    const handlers = this.eventHandlers.get(data.type) || [];
                    handlers.forEach(handler => handler(data.data));
                } catch (error) {
                    console.error('Error parsing SSE message:', error);
                }
            };

            this.connection.onerror = (error) => {
                console.error('SSE Error:', error);
                console.error('Connection state:', this.connection.readyState);
                this.isConnected = false;
                this.handleReconnect();
            };
        } catch (error) {
            console.error('Error creating EventSource:', error);
            this.handleReconnect();
        }
    }

    handleReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.min(1000 * Math.pow(2, this.reconnectAttempts), 30000);
            console.log(`Scheduling reconnect attempt ${this.reconnectAttempts} in ${delay}ms`);
            setTimeout(() => {
                console.log(`Attempting to reconnect (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
                this.connect();
            }, delay);
        } else {
            console.error('Max reconnection attempts reached');
        }
    }

    subscribe(eventType, handler) {
        if (!this.eventHandlers.has(eventType)) {
            this.eventHandlers.set(eventType, []);
        }
        this.eventHandlers.get(eventType).push(handler);
    }

    unsubscribe(eventType, handler) {
        if (this.eventHandlers.has(eventType)) {
            const handlers = this.eventHandlers.get(eventType);
            const index = handlers.indexOf(handler);
            if (index > -1) {
                handlers.splice(index, 1);
            }
        }
    }

    cleanup() {
        if (this.connection) {
            this.connection.close();
            this.connection = null;
        }
        this.eventHandlers.clear();
    }
}

// Create a singleton instance
const sseService = new SSEService();
export default sseService; 