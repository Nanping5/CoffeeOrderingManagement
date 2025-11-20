<template>
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <AdminSidebar />

    <!-- 主要内容区域 -->
    <div class="admin-main">
      <!-- 顶部导航栏 -->
      <AdminHeader />

      <!-- 页面内容 -->
      <main class="admin-content">
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
    </div>
  </div>
</template>

<script setup>
import AdminSidebar from '@/components/admin/AdminSidebar.vue'
import AdminHeader from '@/components/admin/AdminHeader.vue'
</script>

<style lang="scss" scoped>
.admin-layout {
  display: flex;
  height: 100vh;
  background-color: var(--background-color);
}

.admin-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.admin-content {
  flex: 1;
  padding: $spacing-lg;
  overflow-y: auto;
  background-color: var(--background-color);
}

.page-wrapper {
  width: 100%;
  min-height: 100%;
}

// 过渡动画
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

// 响应式设计
@include mobile {
  .admin-layout {
    flex-direction: column;
  }

  .admin-content {
    padding: $spacing-md;
  }
}
</style>