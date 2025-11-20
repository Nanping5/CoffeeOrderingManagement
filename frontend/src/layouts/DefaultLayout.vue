<template>
  <div class="default-layout">
    <!-- 导航栏 -->
    <AppHeader />

    <!-- 主要内容区域 -->
    <main class="main-content">
      <router-view v-slot="{ Component, route }">
        <transition
          name="fade"
          mode="out-in"
          appear
        >
          <div :key="route.path" class="page-wrapper">
            <component :is="Component" />
          </div>
        </transition>
      </router-view>
    </main>

    <!-- 购物车浮动按钮 -->
    <CartFloatButton />

    <!-- 页脚 -->
    <AppFooter />
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import AppHeader from '@/components/common/AppHeader.vue'
import AppFooter from '@/components/common/AppFooter.vue'
import CartFloatButton from '@/components/common/CartFloatButton.vue'
import { useCartStore } from '@/store/cart'

const cartStore = useCartStore()

onMounted(() => {
  // 初始化购物车
  cartStore.initCart()
})
</script>

<style lang="scss" scoped>
.default-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.main-content {
  flex: 1;
  padding: 0;
  background-color: var(--background-color);
}

.page-wrapper {
  width: 100%;
  min-height: calc(100vh - 140px);
}

// 路由过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>