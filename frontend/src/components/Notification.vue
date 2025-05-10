<template>
  <div
    v-if="notification.visible"
    class="notification-popup"
    :class="notification.type"
  >
    <div class="notification-content">
      <span class="desc">{{ notification.message }}</span>
      <button class="close-btn" @click="notification.hide()">&times;</button>
    </div>
  </div>
</template>

<script setup>
import { useNotificationStore } from '@/store/notificationStore';
const notification = useNotificationStore();
</script>

<style scoped>
.notification-popup {
  position: fixed;
  top: 24px;
  right: 24px;
  z-index: 9999;
}
.notification-content {
  background: #232323;
  color: #fff;
  border-radius: 8px;
  padding: 10px 18px 10px 12px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.18);
  display: flex;
  align-items: center;
  min-width: 180px;
  font-size: 1em;
  border-left: 4px solid transparent;
}
.notification-popup.green .notification-content {
  background: #232323;
  border-left: 4px solid #00ff00;
}
.notification-popup.red .notification-content {
  background: #3a1818;
  border-left: 4px solid #ff3b3b;
}
.notification-popup.yellow .notification-content {
  background: #3a2e18;
  border-left: 4px solid #ffe066;
}
.desc {
  flex: 1;
  margin-right: 10px;
}
.close-btn {
  background: none;
  border: none;
  color: #fff;
  font-size: 1.2em;
  cursor: pointer;
  margin-left: 8px;
}
</style>
