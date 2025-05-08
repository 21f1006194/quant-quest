import { defineStore } from 'pinia';

export const useNotificationStore = defineStore('notification', {
    state: () => ({
        visible: false,
        message: '',
        type: '', // 'red', 'green', 'yellow'
    }),
    actions: {
        show(message, type) {
            this.message = message;
            this.type = type;
            this.visible = true;
            console.log('show');
            console.log(this.message, this.type);
        },
        hide() {
            this.visible = false;
            this.message = '';
            this.type = '';
        }
    }
});
