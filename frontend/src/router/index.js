import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/store/auth'

// 布局组件
const DefaultLayout = () => import('@/layouts/DefaultLayout.vue')
const AuthLayout = () => import('@/layouts/AuthLayout.vue')
const AdminLayout = () => import('@/layouts/AdminLayout.vue')

// 页面组件懒加载
const Login = () => import('@/views/LoginPage.vue')
const Register = () => import('@/views/RegisterPage.vue')
const Menu = () => import('@/views/MenuPage.vue')
const Cart = () => import('@/views/CartPage.vue')
const Order = () => import('@/views/OrderPage.vue')
const Profile = () => import('@/views/ProfilePage.vue')
const AdminDashboard = () => import('@/views/admin/DashboardPage.vue')
const AdminMenu = () => import('@/views/admin/MenuManagePage.vue')
const AdminOrders = () => import('@/views/admin/OrderManagePage.vue')
const AdminUsers = () => import('@/views/admin/UserManagePage.vue')
const NotFound = () => import('@/views/NotFoundPage.vue')

const routes = [
  {
    path: '/',
    component: DefaultLayout,
    children: [
      // 根路径重定向
      {
        path: '',
        redirect: '/menu'
      },
      // 用户界面路由
      {
        path: 'menu',
        name: 'Menu',
        component: Menu,
        meta: {
          title: '菜单',
          requiresAuth: false
        }
      },
      {
        path: 'cart',
        name: 'Cart',
        component: Cart,
        meta: {
          title: '购物车',
          requiresAuth: true
        }
      },
      {
        path: 'orders',
        name: 'Orders',
        component: Order,
        meta: {
          title: '我的订单',
          requiresAuth: true
        }
      },
      {
        path: 'profile',
        name: 'Profile',
        component: Profile,
        meta: {
          title: '个人中心',
          requiresAuth: true
        }
      }
    ]
  },
  {
    path: '/',
    component: AuthLayout,
    children: [
      // 认证相关路由
      {
        path: 'login',
        name: 'Login',
        component: Login,
        meta: {
          title: '登录',
          requiresAuth: false
        }
      },
      {
        path: 'register',
        name: 'Register',
        component: Register,
        meta: {
          title: '注册',
          requiresAuth: false
        }
      }
    ]
  },
  {
    path: '/admin',
    component: AdminLayout,
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: AdminDashboard,
        meta: {
          title: '管理后台',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'menu',
        name: 'AdminMenu',
        component: AdminMenu,
        meta: {
          title: '菜单管理',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'orders',
        name: 'AdminOrders',
        component: AdminOrders,
        meta: {
          title: '订单管理',
          requiresAuth: true,
          requiresAdmin: true
        }
      },
      {
        path: 'users',
        name: 'AdminUsers',
        component: AdminUsers,
        meta: {
          title: '用户管理',
          requiresAuth: true,
          requiresAdmin: true
        }
      }
    ]
  },
  // 404页面
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: NotFound,
    meta: {
      title: '页面不存在'
    }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0 }
    }
  }
})

// 全局前置守卫
router.beforeEach(async (to, from, next) => {
  const authStore = useAuthStore()

  // 设置页面标题
  if (to.meta.title) {
    document.title = `${to.meta.title} - ${import.meta.env.VITE_APP_TITLE || '咖啡点餐系统'}`
  }

  // 检查是否需要认证
  if (to.meta.requiresAuth !== false) {
    // 检查是否已登录
    if (!authStore.isAuthenticated) {
      // 尝试从本地存储恢复登录状态
      await authStore.checkAuthStatus()
    }

    // 如果仍然未登录，跳转到登录页
    if (!authStore.isAuthenticated) {
      next({
        name: 'Login',
        query: { redirect: to.fullPath }
      })
      return
    }

    // 检查是否需要管理员权限
    if (to.meta.requiresAdmin && !authStore.isAdmin) {
      // 如果不是管理员，跳转到首页
      next({ name: 'Menu' })
      return
    }
  }

  // 如果已登录用户访问认证页面，跳转到首页
  if (authStore.isAuthenticated && (to.name === 'Login' || to.name === 'Register')) {
    next({ name: 'Menu' })
    return
  }

  next()
})

// 全局后置钩子
router.afterEach((to, from) => {
  // 这里可以添加页面访问统计等逻辑
  console.log(`从 ${from.path} 导航到 ${to.path}`)
})

export default router