import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { createPinia } from 'pinia'

// Import Bootstrap first
import 'bootstrap/dist/css/bootstrap.min.css';
import 'bootstrap/dist/js/bootstrap.bundle.min.js';

// Import our custom styles after Bootstrap
import '@/style.css';

const pinia = createPinia();

createApp(App).use(router).use(pinia).mount('#app')
