<template>
  <div id="app">
    <router-view />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

// 应用初始化时检查登录状态
onMounted(async () => {
  // 检查本地存储的token并自动登录
  await authStore.checkAuthStatus()
})
</script>

<style lang="scss">
// 全局样式已在 styles/index.scss 中定义
</style>