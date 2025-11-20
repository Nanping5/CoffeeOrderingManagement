import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import authApi from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  // 状态
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const refreshToken = ref(localStorage.getItem('refreshToken'))
  const loading = ref(false)

  // 计算属性
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.role === 'admin')
  const userInfo = computed(() => user.value)

  // 方法
  const login = async (credentials) => {
    try {
      loading.value = true
      const response = await authApi.login(credentials)

      if (response.success) {
        // 保存token和用户信息
        token.value = response.access_token
        refreshToken.value = response.refresh_token
        user.value = response.user

        // 持久化存储
        localStorage.setItem('token', response.access_token)
        localStorage.setItem('refreshToken', response.refresh_token)
        localStorage.setItem('user', JSON.stringify(response.user))

        return { success: true, message: response.message }
      } else {
        return { success: false, errors: response.errors }
      }
    } catch (error) {
      console.error('登录失败:', error)
      return { success: false, errors: [error.message || '登录失败'] }
    } finally {
      loading.value = false
    }
  }

  const register = async (userData) => {
    try {
      loading.value = true
      const response = await authApi.register(userData)

      if (response.success) {
        // 保存token和用户信息
        token.value = response.access_token
        refreshToken.value = response.refresh_token
        user.value = response.user

        // 持久化存储
        localStorage.setItem('token', response.access_token)
        localStorage.setItem('refreshToken', response.refresh_token)
        localStorage.setItem('user', JSON.stringify(response.user))

        return { success: true, message: response.message }
      } else {
        return { success: false, errors: response.errors }
      }
    } catch (error) {
      console.error('注册失败:', error)
      return { success: false, errors: [error.message || '注册失败'] }
    } finally {
      loading.value = false
    }
  }

  const logout = () => {
    // 清除状态
    user.value = null
    token.value = null
    refreshToken.value = null

    // 清除本地存储
    localStorage.removeItem('token')
    localStorage.removeItem('refreshToken')
    localStorage.removeItem('user')

    // 调用登出API（可选）
    authApi.logout().catch(console.error)
  }

  const checkAuthStatus = async () => {
    try {
      if (!token.value) {
        // 检查本地存储
        const storedToken = localStorage.getItem('token')
        const storedUser = localStorage.getItem('user')

        if (storedToken && storedUser) {
          token.value = storedToken
          user.value = JSON.parse(storedUser)
          return true
        }
        return false
      }

      // 验证token有效性
      const response = await authApi.verifyToken()
      if (response.success) {
        user.value = response.user
        return true
      } else {
        // token无效，清除状态
        logout()
        return false
      }
    } catch (error) {
      console.error('检查认证状态失败:', error)
      logout()
      return false
    }
  }

  const updateProfile = async (profileData) => {
    try {
      loading.value = true
      const response = await authApi.updateProfile(profileData)

      if (response.success) {
        user.value = response.user
        localStorage.setItem('user', JSON.stringify(response.user))
        return { success: true, message: response.message }
      } else {
        return { success: false, errors: response.errors }
      }
    } catch (error) {
      console.error('更新资料失败:', error)
      return { success: false, errors: [error.message || '更新资料失败'] }
    } finally {
      loading.value = false
    }
  }

  const changePassword = async (passwordData) => {
    try {
      loading.value = true
      const response = await authApi.changePassword(passwordData)

      if (response.success) {
        return { success: true, message: response.message }
      } else {
        return { success: false, errors: response.errors }
      }
    } catch (error) {
      console.error('修改密码失败:', error)
      return { success: false, errors: [error.message || '修改密码失败'] }
    } finally {
      loading.value = false
    }
  }

  const refreshAccessToken = async () => {
    try {
      if (!refreshToken.value) {
        return false
      }

      const response = await authApi.refreshToken()
      if (response.success) {
        token.value = response.access_token
        localStorage.setItem('token', response.access_token)
        return true
      } else {
        logout()
        return false
      }
    } catch (error) {
      console.error('刷新token失败:', error)
      logout()
      return false
    }
  }

  // 初始化时检查认证状态
  const initAuth = async () => {
    await checkAuthStatus()
  }

  return {
    // 状态
    user,
    token,
    refreshToken,
    loading,

    // 计算属性
    isAuthenticated,
    isAdmin,
    userInfo,

    // 方法
    login,
    register,
    logout,
    checkAuthStatus,
    updateProfile,
    changePassword,
    refreshAccessToken,
    initAuth
  }
})