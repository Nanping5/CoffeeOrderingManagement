<template>
  <div class="default-layout">
    <!-- 导航栏 -->
    <AppHeader />

    <!-- 主要内容区域 -->
    <main class="main-content">
      <router-view v-slot="{ Component, route }">
        <transition
          :name="transitionName"
          mode="out-in"
          appear
          @before-enter="handleBeforeEnter"
          @after-enter="handleAfterEnter"
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
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import CartFloatButton from '@/components/CartFloatButton.vue'
import { useCartStore } from '@/store/cart'
import { usePageTransition } from '@/composables/useAnimation'

const route = useRoute()
const cartStore = useCartStore()
const { setPageTransition, getTransitionClass } = usePageTransition()

const transitionName = ref('fade')

// 处理路由过渡
watch(() => route.path, (newPath, oldPath) => {
  const fromRoute = oldPath?.split('/').pop() || 'unknown'
  const toRoute = newPath?.split('/').pop() || 'unknown'

  setPageTransition(fromRoute, toRoute)
  transitionName.value = getTransitionClass()
}, { immediate: true })

// 页面进入前处理
const handleBeforeEnter = () => {
  // 添加页面加载类
  document.body.classList.add('page-loading')
}

// 页面进入后处理
const handleAfterEnter = () => {
  // 移除页面加载类
  document.body.classList.remove('page-loading')
}

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
  position: relative;
}

.page-wrapper {
  width: 100%;
  min-height: calc(100vh - 140px);
}

// 页面加载状态
:global(.page-loading) {
  overflow: hidden;
}

// 路由过渡动画
.transition-fade-enter-active,
.transition-fade-leave-active {
  transition: opacity 0.3s ease;
}

.transition-fade-enter-from,
.transition-fade-leave-to {
  opacity: 0;
}

// 从左滑入
.transition-slide-left-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-slide-left-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-slide-left-enter-from {
  opacity: 0;
  transform: translateX(30px);
}

.transition-slide-left-leave-to {
  opacity: 0;
  transform: translateX(-30px);
}

// 从右滑入
.transition-slide-right-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-slide-right-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-slide-right-enter-from {
  opacity: 0;
  transform: translateX(-30px);
}

.transition-slide-right-leave-to {
  opacity: 0;
  transform: translateX(30px);
}

// 从下滑入
.transition-slide-up-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-slide-up-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-slide-up-enter-from {
  opacity: 0;
  transform: translateY(30px);
}

.transition-slide-up-leave-to {
  opacity: 0;
  transform: translateY(-30px);
}

// 从上滑入
.transition-slide-down-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-slide-down-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-slide-down-enter-from {
  opacity: 0;
  transform: translateY(-30px);
}

.transition-slide-down-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

// 缩放过渡
.transition-scale-enter-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-scale-leave-active {
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-scale-enter-from {
  opacity: 0;
  transform: scale(0.9);
}

.transition-scale-leave-to {
  opacity: 0;
  transform: scale(1.1);
}

// 翻转过渡
.transition-flip-enter-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-flip-leave-active {
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
}

.transition-flip-enter-from {
  opacity: 0;
  transform: perspective(800px) rotateY(-90deg);
}

.transition-flip-leave-to {
  opacity: 0;
  transform: perspective(800px) rotateY(90deg);
}
</style>