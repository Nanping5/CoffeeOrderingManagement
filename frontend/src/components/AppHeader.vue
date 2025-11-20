<template>
  <header class="app-header" :class="{ 'header-scrolled': isScrolled }">
    <div class="header-container">
      <!-- Logo区域 -->
      <div class="logo-section">
        <router-link to="/" class="logo-link">
          <div class="logo">
            <el-icon class="logo-icon"><Coffee /></el-icon>
            <span class="logo-text">咖啡时光</span>
          </div>
        </router-link>
      </div>

      <!-- 导航菜单 -->
      <nav class="nav-section">
        <el-menu
          :default-active="activeRoute"
          mode="horizontal"
          :ellipsis="false"
          class="nav-menu"
          @select="handleMenuSelect"
        >
          <el-menu-item index="menu">
            <el-icon><Coffee /></el-icon>
            <span>菜单</span>
          </el-menu-item>

          <el-menu-item v-if="authStore.isAuthenticated" index="orders">
            <el-icon><List /></el-icon>
            <span>我的订单</span>
          </el-menu-item>

          <el-menu-item v-if="authStore.isAdmin" index="admin">
            <el-icon><Setting /></el-icon>
            <span>管理后台</span>
          </el-menu-item>
        </el-menu>
      </nav>

      <!-- 用户操作区域 -->
      <div class="user-section">
        <!-- 搜索按钮（移动端） -->
        <el-button
          v-if="isMobile"
          type="text"
          :icon="Search"
          @click="showMobileSearch = true"
          class="mobile-search-btn"
        />

        <!-- 购物车按钮 -->
        <el-badge
          :value="cartItemsCount"
          :hidden="cartItemsCount === 0"
          class="cart-badge"
        >
          <el-button
            type="text"
            :icon="ShoppingCart"
            @click="handleCartClick"
            class="cart-btn"
            :class="{ 'cart-btn-active': $route.name === 'Cart' }"
          >
            <span v-if="!isMobile">购物车</span>
          </el-button>
        </el-badge>

        <!-- 用户菜单 -->
        <el-dropdown v-if="authStore.isAuthenticated" @command="handleUserCommand">
          <div class="user-dropdown">
            <el-avatar :size="36" :src="userAvatar" class="user-avatar">
              <el-icon><User /></el-icon>
            </el-avatar>
            <span v-if="!isMobile" class="user-name">{{ userName }}</span>
            <el-icon class="dropdown-icon"><ArrowDown /></el-icon>
          </div>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item command="profile">
                <el-icon><User /></el-icon>
                个人中心
              </el-dropdown-item>
              <el-dropdown-item command="orders">
                <el-icon><List /></el-icon>
                我的订单
              </el-dropdown-item>
              <el-dropdown-item v-if="authStore.isAdmin" command="admin">
                <el-icon><Setting /></el-icon>
                管理后台
              </el-dropdown-item>
              <el-dropdown-item divided command="logout">
                <el-icon><SwitchButton /></el-icon>
                退出登录
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>

        <!-- 登录/注册按钮（未登录状态） -->
        <div v-else class="auth-buttons">
          <el-button
            type="text"
            @click="handleLogin"
            class="login-btn"
          >
            登录
          </el-button>
          <el-button
            type="primary"
            @click="handleRegister"
            class="register-btn"
          >
            注册
          </el-button>
        </div>
      </div>

      <!-- 移动端菜单按钮 -->
      <el-button
        v-if="isMobile"
        type="text"
        :icon="isMobileMenuOpen ? Close : Menu"
        @click="toggleMobileMenu"
        class="mobile-menu-btn"
      />
    </div>

    <!-- 移动端导航菜单 -->
    <transition name="slide-down">
      <div v-if="isMobile && isMobileMenuOpen" class="mobile-nav-menu">
        <el-menu
          :default-active="activeRoute"
          @select="handleMobileMenuSelect"
        >
          <el-menu-item index="menu">
            <el-icon><Coffee /></el-icon>
            <span>菜单</span>
          </el-menu-item>
          <el-menu-item v-if="authStore.isAuthenticated" index="orders">
            <el-icon><List /></el-icon>
            <span>我的订单</span>
          </el-menu-item>
          <el-menu-item v-if="authStore.isAdmin" index="admin">
            <el-icon><Setting /></el-icon>
            <span>管理后台</span>
          </el-menu-item>
        </el-menu>
      </div>
    </transition>

    <!-- 移动端搜索弹窗 -->
    <el-dialog
      v-model="showMobileSearch"
      title="搜索"
      :show-close="false"
      class="mobile-search-dialog"
      align-center
    >
      <el-input
        v-model="mobileSearchQuery"
        placeholder="搜索您喜欢的咖啡..."
        prefix-icon="Search"
        clearable
        @keyup.enter="handleMobileSearch"
        ref="mobileSearchInput"
      />
      <template #footer>
        <el-button @click="showMobileSearch = false">取消</el-button>
        <el-button type="primary" @click="handleMobileSearch">搜索</el-button>
      </template>
    </el-dialog>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessageBox, ElMessage } from 'element-plus'
import {
  Coffee,
  ShoppingCart,
  Search,
  User,
  ArrowDown,
  SwitchButton,
  List,
  Setting,
  Menu,
  Close
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { useCartStore } from '@/store/cart'

// 路由和状态管理
const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

// 响应式数据
const isScrolled = ref(false)
const isMobile = ref(false)
const isMobileMenuOpen = ref(false)
const showMobileSearch = ref(false)
const mobileSearchQuery = ref('')
const mobileSearchInput = ref(null)

// 计算属性
const activeRoute = computed(() => {
  // 管理页面路由特殊处理
  if (route.path.startsWith('/admin')) {
    return 'admin'
  }
  return route.name?.toLowerCase() || 'menu'
})

const userName = computed(() => {
  return authStore.user?.username || authStore.user?.email || '用户'
})

const userAvatar = computed(() => {
  return authStore.user?.avatar || ''
})

const cartItemsCount = computed(() => {
  return cartStore.totalItems
})

// 方法
const handleScroll = () => {
  isScrolled.value = window.scrollY > 50
}

const checkMobile = () => {
  isMobile.value = window.innerWidth <= 768
  if (!isMobile.value) {
    isMobileMenuOpen.value = false
  }
}

const handleMenuSelect = (index) => {
  navigateToRoute(index)
}

const handleMobileMenuSelect = (index) => {
  isMobileMenuOpen.value = false
  navigateToRoute(index)
}

const navigateToRoute = (index) => {
  switch (index) {
    case 'menu':
      router.push('/menu')
      break
    case 'orders':
      router.push('/orders')
      break
    case 'admin':
      router.push('/admin')
      break
  }
}

const handleCartClick = () => {
  if (!authStore.isAuthenticated) {
    ElMessageBox.confirm(
      '请先登录后再查看购物车',
      '提示',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'info'
      }
    ).then(() => {
      router.push('/login')
    }).catch(() => {
      // 用户取消
    })
    return
  }
  router.push('/cart')
}

const handleUserCommand = (command) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'orders':
      router.push('/orders')
      break
    case 'admin':
      router.push('/admin')
      break
    case 'logout':
      handleLogout()
      break
  }
}

const handleLogin = () => {
  authStore.setRedirectPath(route.fullPath)
  router.push('/login')
}

const handleRegister = () => {
  authStore.setRedirectPath(route.fullPath)
  router.push('/register')
}

const handleLogout = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要退出登录吗？',
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await authStore.logout()
    ElMessage.success('已成功退出登录')

    // 跳转到首页
    router.push('/menu')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('退出登录失败:', error)
      ElMessage.error('退出登录失败，请稍后重试')
    }
  }
}

const toggleMobileMenu = () => {
  isMobileMenuOpen.value = !isMobileMenuOpen.value
}

const handleMobileSearch = () => {
  if (mobileSearchQuery.value.trim()) {
    // 跳转到菜单页面并传递搜索参数
    router.push({
      path: '/menu',
      query: { search: mobileSearchQuery.value.trim() }
    })
    showMobileSearch.value = false
    mobileSearchQuery.value = ''
  }
}

// 监听移动端搜索弹窗显示
watch(showMobileSearch, (newVal) => {
  if (newVal) {
    nextTick(() => {
      mobileSearchInput.value?.focus()
    })
  }
})

// 生命周期
onMounted(() => {
  checkMobile()
  window.addEventListener('scroll', handleScroll)
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('resize', checkMobile)
})
</script>

<style lang="scss" scoped>
.app-header {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  z-index: 1000;
  transition: all 0.3s ease;

  &.header-scrolled {
    background: rgba(255, 255, 255, 0.98);
    box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  }
}

.header-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

// Logo区域
.logo-section {
  .logo-link {
    text-decoration: none;
    color: inherit;
  }

  .logo {
    display: flex;
    align-items: center;
    gap: 10px;
    font-size: 1.5rem;
    font-weight: bold;
    color: #8b4513;
    transition: transform 0.3s ease;

    &:hover {
      transform: scale(1.05);
    }

    .logo-icon {
      font-size: 2rem;
      color: #8b4513;
    }

    .logo-text {
      background: linear-gradient(135deg, #8b4513, #a0522d);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
      background-clip: text;
    }
  }
}

// 导航菜单
.nav-section {
  flex: 1;
  display: flex;
  justify-content: center;

  :deep(.nav-menu) {
    border: none;
    background: transparent;

    .el-menu-item {
      border-radius: 8px;
      margin: 0 8px;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(139, 69, 19, 0.1);
        color: #8b4513;
      }

      &.is-active {
        background: linear-gradient(135deg, #8b4513, #a0522d);
        color: white;

        .el-icon {
          color: white;
        }
      }
    }
  }
}

// 用户操作区域
.user-section {
  display: flex;
  align-items: center;
  gap: 16px;

  .mobile-search-btn {
    font-size: 1.2rem;
    color: #8b4513;

    &:hover {
      background: rgba(139, 69, 19, 0.1);
    }
  }

  .cart-badge {
    :deep(.el-badge__content) {
      background: #e74c3c;
      border: 2px solid white;
    }

    .cart-btn {
      display: flex;
      align-items: center;
      gap: 6px;
      font-size: 1rem;
      color: #8b4513;
      padding: 8px 12px;
      border-radius: 8px;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(139, 69, 19, 0.1);
        color: #a0522d;
      }

      &.cart-btn-active {
        background: linear-gradient(135deg, #8b4513, #a0522d);
        color: white;
      }
    }
  }

  .user-dropdown {
    display: flex;
    align-items: center;
    gap: 8px;
    padding: 6px 12px;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;

    &:hover {
      background: rgba(139, 69, 19, 0.1);
    }

    .user-avatar {
      border: 2px solid #8b4513;
    }

    .user-name {
      font-size: 0.9rem;
      color: #2c3e50;
      font-weight: 500;
    }

    .dropdown-icon {
      font-size: 0.8rem;
      color: #7f8c8d;
      transition: transform 0.3s ease;
    }

    &:hover .dropdown-icon {
      transform: translateY(2px);
    }
  }

  .auth-buttons {
    display: flex;
    gap: 12px;

    .login-btn {
      color: #8b4513;
      border: 1px solid #8b4513;
      border-radius: 20px;
      padding: 8px 20px;
      transition: all 0.3s ease;

      &:hover {
        background: rgba(139, 69, 19, 0.1);
      }
    }

    .register-btn {
      background: linear-gradient(135deg, #8b4513, #a0522d);
      border: none;
      border-radius: 20px;
      padding: 8px 20px;
      transition: all 0.3s ease;

      &:hover {
        background: linear-gradient(135deg, #a0522d, #8b4513);
        transform: translateY(-2px);
      }
    }
  }

  .mobile-menu-btn {
    font-size: 1.2rem;
    color: #8b4513;

    &:hover {
      background: rgba(139, 69, 19, 0.1);
    }
  }
}

// 移动端导航菜单
.mobile-nav-menu {
  position: absolute;
  top: 100%;
  left: 0;
  right: 0;
  background: white;
  border-bottom: 1px solid rgba(0, 0, 0, 0.1);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

  :deep(.el-menu) {
    border: none;

    .el-menu-item {
      &:hover {
        background: rgba(139, 69, 19, 0.1);
        color: #8b4513;
      }

      &.is-active {
        background: linear-gradient(135deg, #8b4513, #a0522d);
        color: white;
      }
    }
  }
}

// 移动端搜索弹窗
:deep(.mobile-search-dialog) {
  .el-dialog {
    border-radius: 12px;
    margin: 20px;
  }

  .el-dialog__header {
    padding: 16px 20px 0;
  }

  .el-dialog__body {
    padding: 16px 20px;
  }

  .el-dialog__footer {
    padding: 0 20px 16px;
  }
}

// 动画
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.3s ease;
}

.slide-down-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}

.slide-down-leave-to {
  transform: translateY(-100%);
  opacity: 0;
}

// 响应式设计
@media (max-width: 768px) {
  .header-container {
    padding: 0 16px;
    height: 56px;
  }

  .logo-section {
    .logo {
      font-size: 1.3rem;

      .logo-icon {
        font-size: 1.8rem;
      }

      .logo-text {
        font-size: 1.2rem;
      }
    }
  }

  .nav-section {
    display: none;
  }

  .user-section {
    gap: 12px;

    .cart-btn span {
      display: none;
    }

    .auth-buttons {
      .login-btn,
      .register-btn {
        padding: 6px 12px;
        font-size: 0.9rem;
      }
    }
  }
}

@media (max-width: 480px) {
  .header-container {
    padding: 0 12px;
  }

  .logo-section {
    .logo {
      .logo-text {
        display: none;
      }
    }
  }

  .user-section {
    gap: 8px;
  }
}
</style>