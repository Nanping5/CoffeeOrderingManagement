import request from './index'

export default {
  // 用户登录
  login(credentials) {
    return request.post('/auth/login', credentials)
  },

  // 用户注册
  register(userData) {
    return request.post('/auth/register', userData)
  },

  // 刷新Token
  refreshToken() {
    return request.post('/auth/refresh')
  },

  // 获取用户资料
  getProfile() {
    return request.get('/auth/profile')
  },

  // 更新用户资料
  updateProfile(profileData) {
    return request.put('/auth/profile', profileData)
  },

  // 修改密码
  changePassword(passwordData) {
    return request.post('/auth/change-password', passwordData)
  },

  // 登出
  logout() {
    return request.post('/auth/logout')
  },

  // 验证Token
  verifyToken() {
    return request.get('/auth/verify-token')
  },

  // 获取当前用户基本信息
  getUserInfo() {
    return request.get('/auth/user-info')
  }
}