<template>
  <div class="auth-layout">
    <div class="auth-container">
      <!-- 左侧装饰区域 -->
      <div class="auth-left">
        <div class="brand-info">
          <div class="brand-logo">
            <img src="/coffee-logo.svg" alt="Coffee Logo" class="logo-image" />
          </div>
          <h1 class="brand-title animate__animated animate__fadeInDown">
            咖啡点餐系统
          </h1>
          <p class="brand-subtitle animate__animated animate__fadeInUp">
            享受每一杯咖啡的美好时光
          </p>
          <div class="features animate__animated animate__fadeInUp animate__delay-1s">
            <div class="feature-item">
              <el-icon><Coffee /></el-icon>
              <span>精选咖啡豆</span>
            </div>
            <div class="feature-item">
              <el-icon><Timer /></el-icon>
              <span>快速配送</span>
            </div>
            <div class="feature-item">
              <el-icon><Service /></el-icon>
              <span>优质服务</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 右侧登录表单区域 -->
      <div class="auth-right">
        <div class="auth-form-container">
          <router-view v-slot="{ Component, route }">
            <transition
              name="slide-fade"
              mode="out-in"
              appear
            >
              <component :is="Component" :key="route.path" />
            </transition>
          </router-view>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { Coffee, Timer, Service } from '@element-plus/icons-vue'
</script>

<style lang="scss" scoped>
.auth-layout {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
  padding: $spacing-lg;
}

.auth-container {
  display: flex;
  width: 100%;
  max-width: 1200px;
  min-height: 600px;
  background: var(--white);
  border-radius: $border-radius-large;
  box-shadow: $shadow-heavy;
  overflow: hidden;
}

.auth-left {
  flex: 1;
  background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
  color: var(--white);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
  position: relative;

  @include mobile {
    display: none;
  }

  &::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: url('/coffee-pattern.svg') repeat;
    opacity: 0.1;
  }
}

.brand-info {
  text-align: center;
  z-index: 1;
}

.brand-logo {
  margin-bottom: $spacing-lg;
  .logo-image {
    width: 80px;
    height: 80px;
    filter: brightness(0) invert(1);
  }
}

.brand-title {
  font-size: var(--font-size-xxl);
  font-weight: 700;
  margin-bottom: $spacing-md;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
}

.brand-subtitle {
  font-size: var(--font-size-lg);
  opacity: 0.9;
  margin-bottom: $spacing-xl;
  line-height: 1.6;
}

.features {
  display: flex;
  flex-direction: column;
  gap: $spacing-md;
}

.feature-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: $spacing-sm;
  font-size: var(--font-size-md);
  opacity: 0.9;

  .el-icon {
    font-size: 20px;
  }
}

.auth-right {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
  background-color: var(--background-color);
}

.auth-form-container {
  width: 100%;
  max-width: 400px;
}

// 过渡动画
.slide-fade-enter-active {
  transition: all 0.3s ease-out;
}

.slide-fade-leave-active {
  transition: all 0.3s cubic-bezier(1, 0.5, 0.8, 1);
}

.slide-fade-enter-from {
  transform: translateX(20px);
  opacity: 0;
}

.slide-fade-leave-to {
  transform: translateX(-20px);
  opacity: 0;
}

// 响应式设计
@include mobile {
  .auth-container {
    max-width: 400px;
    min-height: auto;
  }

  .auth-right {
    padding: $spacing-lg;
  }
}
</style>