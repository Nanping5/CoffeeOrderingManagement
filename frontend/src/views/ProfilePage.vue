<template>
  <div class="profile-page">
    <!-- 页面头部 -->
    <div class="page-header animate__animated animate__fadeInDown">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><User /></el-icon>
          个人中心
        </h1>
        <p class="page-subtitle">管理您的个人信息和偏好设置</p>
      </div>
    </div>

    <div class="profile-container">
      <el-row :gutter="24">
        <!-- 左侧：个人信息和导航 -->
        <el-col :xs="24" :md="8">
          <div class="profile-sidebar">
            <!-- 用户信息卡片 -->
            <el-card class="user-card animate__animated animate__fadeInLeft">
              <div class="user-info">
                <!-- 头像上传 -->
                <div class="avatar-section">
                  <el-upload
                    class="avatar-uploader"
                    action="#"
                    :show-file-list="false"
                    :before-upload="beforeAvatarUpload"
                    :http-request="handleAvatarUpload"
                  >
                    <img
                      v-if="userInfo.avatar"
                      :src="userInfo.avatar"
                      class="avatar"
                      alt="用户头像"
                    />
                    <el-icon v-else class="avatar-uploader-icon"><Plus /></el-icon>
                  </el-upload>
                  <div class="avatar-status">
                    <el-tag type="success" size="small">已认证</el-tag>
                  </div>
                </div>

                <!-- 用户基本信息 -->
                <div class="user-details">
                  <h3 class="user-name">{{ userInfo.username || '用户' }}</h3>
                  <p class="user-email">{{ userInfo.email }}</p>
                  <div class="user-meta">
                    <span class="join-date">
                      加入时间：{{ formatDate(userInfo.created_at) }}
                    </span>
                    <span class="user-level">
                      <el-tag type="warning" size="small">
                        {{ getUserLevel(userInfo.order_count) }}
                      </el-tag>
                    </span>
                  </div>
                </div>

                <!-- 操作按钮 -->
                <div class="user-actions">
                  <el-button
                    type="primary"
                    :icon="Edit"
                    @click="editProfileVisible = true"
                    class="edit-btn"
                  >
                    编辑资料
                  </el-button>
                  <el-button
                    :icon="Lock"
                    @click="changePasswordVisible = true"
                    class="password-btn"
                  >
                    修改密码
                  </el-button>
                </div>
              </div>
            </el-card>

            <!-- 导航菜单 -->
            <el-card class="nav-card animate__animated animate__fadeInLeft" style="animation-delay: 100ms">
              <el-menu
                :default-active="activeTab"
                @select="handleTabSelect"
                class="profile-menu"
              >
                <el-menu-item index="overview">
                  <el-icon><Odometer /></el-icon>
                  <span>数据概览</span>
                </el-menu-item>
                <el-menu-item index="orders">
                  <el-icon><List /></el-icon>
                  <span>订单记录</span>
                </el-menu-item>
                <el-menu-item index="favorites">
                  <el-icon><Star /></el-icon>
                  <span>我的收藏</span>
                </el-menu-item>
                <el-menu-item index="addresses">
                  <el-icon><LocationInformation /></el-icon>
                  <span>收货地址</span>
                </el-menu-item>
                <el-menu-item index="settings">
                  <el-icon><Setting /></el-icon>
                  <span>偏好设置</span>
                </el-menu-item>
                <el-menu-item index="notifications">
                  <el-icon><Bell /></el-icon>
                  <span>消息通知</span>
                </el-menu-item>
              </el-menu>
            </el-card>
          </div>
        </el-col>

        <!-- 右侧：内容区域 -->
        <el-col :xs="24" :md="16">
          <div class="profile-content">
            <!-- 数据概览 -->
            <div v-if="activeTab === 'overview'" class="content-section animate__animated animate__fadeInRight">
              <el-card class="overview-card">
                <template #header>
                  <h3>数据概览</h3>
                </template>

                <el-row :gutter="20">
                  <el-col :xs="12" :sm="6">
                    <div class="stat-item">
                      <div class="stat-icon">
                        <el-icon><ShoppingCart /></el-icon>
                      </div>
                      <div class="stat-info">
                        <div class="stat-value">{{ userStats.total_orders || 0 }}</div>
                        <div class="stat-label">总订单</div>
                      </div>
                    </div>
                  </el-col>
                  <el-col :xs="12" :sm="6">
                    <div class="stat-item">
                      <div class="stat-icon">
                        <el-icon><Coffee /></el-icon>
                      </div>
                      <div class="stat-info">
                        <div class="stat-value">{{ userStats.total_items || 0 }}</div>
                        <div class="stat-label">总商品</div>
                      </div>
                    </div>
                  </el-col>
                  <el-col :xs="12" :sm="6">
                    <div class="stat-item">
                      <div class="stat-icon">
                        <el-icon><Money /></el-icon>
                      </div>
                      <div class="stat-info">
                        <div class="stat-value">¥{{ (userStats.total_spent || 0).toFixed(2) }}</div>
                        <div class="stat-label">总消费</div>
                      </div>
                    </div>
                  </el-col>
                  <el-col :xs="12" :sm="6">
                    <div class="stat-item">
                      <div class="stat-icon">
                        <el-icon><Star /></el-icon>
                      </div>
                      <div class="stat-info">
                        <div class="stat-value">{{ userStats.favorite_items || 0 }}</div>
                        <div class="stat-label">收藏商品</div>
                      </div>
                    </div>
                  </el-col>
                </el-row>

                <!-- 最近订单 -->
                <div class="recent-orders" v-if="recentOrders.length > 0">
                  <h4>最近订单</h4>
                  <div class="order-list">
                    <div
                      v-for="order in recentOrders"
                      :key="order.id"
                      class="order-item"
                      @click="viewOrderDetail(order)"
                    >
                      <div class="order-info">
                        <span class="order-number">{{ order.order_number }}</span>
                        <span class="order-time">{{ formatDate(order.created_at) }}</span>
                      </div>
                      <div class="order-amount">¥{{ order.total_price.toFixed(2) }}</div>
                      <el-tag
                        :type="getStatusType(order.status)"
                        size="small"
                      >
                        {{ getStatusLabel(order.status) }}
                      </el-tag>
                    </div>
                  </div>
                </div>
              </el-card>
            </div>

            <!-- 订单记录 -->
            <div v-else-if="activeTab === 'orders'" class="content-section animate__animated animate__fadeInRight">
              <el-card class="orders-card">
                <template #header>
                  <div class="card-header">
                    <h3>订单记录</h3>
                    <el-button
                      type="primary"
                      @click="goToOrders"
                      class="view-all-btn"
                    >
                      查看全部
                    </el-button>
                  </div>
                </template>

                <div class="orders-content">
                  <div v-if="orderHistory.length === 0" class="empty-orders">
                    <el-empty description="暂无订单记录">
                      <el-button type="primary" @click="goToMenu">
                        去点餐
                      </el-button>
                    </el-empty>
                  </div>
                  <div v-else class="order-history-list">
                    <div
                      v-for="order in orderHistory"
                      :key="order.id"
                      class="order-history-item"
                    >
                      <div class="order-header">
                        <span class="order-number">{{ order.order_number }}</span>
                        <el-tag
                          :type="getStatusType(order.status)"
                          size="small"
                        >
                          {{ getStatusLabel(order.status) }}
                        </el-tag>
                      </div>
                      <div class="order-content">
                        <div class="order-items-preview">
                          <img
                            v-for="item in order.items.slice(0, 3)"
                            :key="item.id"
                            :src="item.image_url || '/default-coffee.jpg'"
                            :alt="item.name"
                            class="item-preview"
                          />
                          <span v-if="order.items.length > 3" class="more-items">
                            +{{ order.items.length - 3 }}
                          </span>
                        </div>
                        <div class="order-details">
                          <span class="order-time">{{ formatDate(order.created_at) }}</span>
                          <span class="order-amount">¥{{ order.total_price.toFixed(2) }}</span>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </el-card>
            </div>

            <!-- 我的收藏 -->
            <div v-else-if="activeTab === 'favorites'" class="content-section animate__animated animate__fadeInRight">
              <el-card class="favorites-card">
                <template #header>
                  <h3>我的收藏</h3>
                </template>

                <div v-if="favoriteItems.length === 0" class="empty-favorites">
                  <el-empty description="暂无收藏商品">
                    <el-button type="primary" @click="goToMenu">
                      去收藏商品
                    </el-button>
                  </el-empty>
                </div>
                <div v-else class="favorites-grid">
                  <div
                    v-for="item in favoriteItems"
                    :key="item.id"
                    class="favorite-item"
                  >
                    <CoffeeCard
                      :item="item"
                      :show-quick-actions="true"
                      @add-to-cart="handleAddToCart"
                      @remove-favorite="handleRemoveFavorite"
                    />
                  </div>
                </div>
              </el-card>
            </div>

            <!-- 收货地址 -->
            <div v-else-if="activeTab === 'addresses'" class="content-section animate__animated animate__fadeInRight">
              <el-card class="addresses-card">
                <template #header>
                  <div class="card-header">
                    <h3>收货地址</h3>
                    <el-button
                      type="primary"
                      :icon="Plus"
                      @click="addAddressVisible = true"
                      class="add-btn"
                    >
                      添加地址
                    </el-button>
                  </div>
                </template>

                <div v-if="addresses.length === 0" class="empty-addresses">
                  <el-empty description="暂无收货地址">
                    <el-button
                      type="primary"
                      @click="addAddressVisible = true"
                    >
                      添加收货地址
                    </el-button>
                  </el-empty>
                </div>
                <div v-else class="addresses-list">
                  <div
                    v-for="address in addresses"
                    :key="address.id"
                    class="address-item"
                    :class="{ 'default-address': address.is_default }"
                  >
                    <div class="address-content">
                      <div class="address-header">
                        <span class="contact-name">{{ address.contact_name }}</span>
                        <span class="contact-phone">{{ address.phone }}</span>
                        <el-tag v-if="address.is_default" type="success" size="small">默认地址</el-tag>
                      </div>
                      <div class="address-detail">
                        {{ address.full_address }}
                      </div>
                    </div>
                    <div class="address-actions">
                      <el-button
                        type="text"
                        size="small"
                        @click="editAddress(address)"
                      >
                        编辑
                      </el-button>
                      <el-button
                        v-if="!address.is_default"
                        type="text"
                        size="small"
                        @click="setDefaultAddress(address)"
                      >
                        设为默认
                      </el-button>
                      <el-button
                        type="text"
                        size="small"
                        @click="deleteAddress(address)"
                        class="delete-btn"
                      >
                        删除
                      </el-button>
                    </div>
                  </div>
                </div>
              </el-card>
            </div>

            <!-- 其他标签页的占位内容 -->
            <div v-else class="content-section animate__animated animate__fadeInRight">
              <el-card>
                <template #header>
                  <h3>{{ getTabTitle(activeTab) }}</h3>
                </template>
                <div class="placeholder-content">
                  <el-empty description="功能开发中..." />
                </div>
              </el-card>
            </div>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 编辑资料弹窗 -->
    <el-dialog
      v-model="editProfileVisible"
      title="编辑个人资料"
      width="500px"
      class="profile-dialog"
    >
      <el-form
        ref="editProfileForm"
        :model="editForm"
        :rules="editRules"
        label-width="80px"
      >
        <el-form-item label="用户名" prop="username">
          <el-input
            v-model="editForm.username"
            placeholder="请输入用户名"
          />
        </el-form-item>
        <el-form-item label="邮箱" prop="email">
          <el-input
            v-model="editForm.email"
            placeholder="请输入邮箱"
            disabled
          />
        </el-form-item>
        <el-form-item label="手机号" prop="phone">
          <el-input
            v-model="editForm.phone"
            placeholder="请输入手机号"
          />
        </el-form-item>
        <el-form-item label="性别" prop="gender">
          <el-radio-group v-model="editForm.gender">
            <el-radio label="male">男</el-radio>
            <el-radio label="female">女</el-radio>
            <el-radio label="other">其他</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="生日" prop="birthday">
          <el-date-picker
            v-model="editForm.birthday"
            type="date"
            placeholder="选择生日"
            format="YYYY-MM-DD"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editProfileVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="saveProfile"
          :loading="savingProfile"
        >
          保存
        </el-button>
      </template>
    </el-dialog>

    <!-- 修改密码弹窗 -->
    <el-dialog
      v-model="changePasswordVisible"
      title="修改密码"
      width="450px"
      class="password-dialog"
    >
      <el-form
        ref="passwordForm"
        :model="passwordForm"
        :rules="passwordRules"
        label-width="100px"
      >
        <el-form-item label="当前密码" prop="current_password">
          <el-input
            v-model="passwordForm.current_password"
            type="password"
            placeholder="请输入当前密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="新密码" prop="new_password">
          <el-input
            v-model="passwordForm.new_password"
            type="password"
            placeholder="请输入新密码"
            show-password
          />
        </el-form-item>
        <el-form-item label="确认密码" prop="confirm_password">
          <el-input
            v-model="passwordForm.confirm_password"
            type="password"
            placeholder="请再次输入新密码"
            show-password
          />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="changePasswordVisible = false">取消</el-button>
        <el-button
          type="primary"
          @click="changePassword"
          :loading="changingPassword"
        >
          确认修改
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  User,
  Edit,
  Lock,
  Plus,
  Odometer,
  List,
  Star,
  LocationInformation,
  Setting,
  Bell,
  ShoppingCart,
  Coffee,
  Money,
  Timer,
  SuccessFilled,
  Warning,
  CircleClose
} from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'
import { useCartStore } from '@/store/cart'
import orderAPI from '@/api/order'
import menuAPI from '@/api/menu'
import authAPI from '@/api/auth'
import CoffeeCard from '@/components/CoffeeCard.vue'

// 路由和状态管理
const router = useRouter()
const authStore = useAuthStore()
const cartStore = useCartStore()

// 响应式数据
const activeTab = ref('overview')
const userInfo = ref({})
const userStats = ref({})
const recentOrders = ref([])
const orderHistory = ref([])
const favoriteItems = ref([])
const addresses = ref([])

// 弹窗状态
const editProfileVisible = ref(false)
const changePasswordVisible = ref(false)
const addAddressVisible = ref(false)
const savingProfile = ref(false)
const changingPassword = ref(false)

// 表单数据
const editForm = reactive({
  username: '',
  email: '',
  phone: '',
  gender: 'other',
  birthday: ''
})

const passwordForm = reactive({
  current_password: '',
  new_password: '',
  confirm_password: ''
})

// 表单验证规则
const editRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 2, max: 20, message: '用户名长度在 2 到 20 个字符', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur' }
  ]
}

const passwordRules = {
  current_password: [
    { required: true, message: '请输入当前密码', trigger: 'blur' }
  ],
  new_password: [
    { required: true, message: '请输入新密码', trigger: 'blur' },
    { min: 6, message: '密码长度至少6位', trigger: 'blur' }
  ],
  confirm_password: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== passwordForm.new_password) {
          callback(new Error('两次输入密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 计算属性
const getStatusType = (status) => {
  const typeMap = {
    'pending': 'warning',
    'processing': 'info',
    'delivering': 'primary',
    'completed': 'success',
    'cancelled': 'danger'
  }
  return typeMap[status] || 'info'
}

const getStatusLabel = (status) => {
  const labelMap = {
    'pending': '待处理',
    'processing': '处理中',
    'delivering': '配送中',
    'completed': '已完成',
    'cancelled': '已取消'
  }
  return labelMap[status] || status
}

// 方法
const formatDate = (dateString) => {
  if (!dateString) return '-'
  return new Date(dateString).toLocaleDateString('zh-CN')
}

const getUserLevel = (orderCount) => {
  if (orderCount >= 50) return '咖啡达人'
  if (orderCount >= 20) return '咖啡爱好者'
  if (orderCount >= 5) return '咖啡新手'
  return '新用户'
}

const handleTabSelect = (key) => {
  activeTab.value = key
  loadTabContent(key)
}

const loadTabContent = async (tab) => {
  switch (tab) {
    case 'orders':
      await loadOrderHistory()
      break
    case 'favorites':
      await loadFavoriteItems()
      break
    case 'addresses':
      await loadAddresses()
      break
  }
}

const loadUserInfo = async () => {
  try {
    const response = await authAPI.getUserProfile()
    userInfo.value = response.data

    // 填充编辑表单
    Object.keys(editForm).forEach(key => {
      editForm[key] = userInfo.value[key] || editForm[key]
    })
  } catch (error) {
    console.error('获取用户信息失败:', error)
  }
}

const loadUserStats = async () => {
  try {
    const response = await orderAPI.getUserStatistics()
    userStats.value = response.data
  } catch (error) {
    console.error('获取用户统计失败:', error)
  }
}

const loadRecentOrders = async () => {
  try {
    const response = await orderAPI.getMyOrders({ page: 1, page_size: 5 })
    recentOrders.value = response.data.items || []
  } catch (error) {
    console.error('获取最近订单失败:', error)
  }
}

const loadOrderHistory = async () => {
  try {
    const response = await orderAPI.getMyOrders({ page: 1, page_size: 10 })
    orderHistory.value = response.data.items || []
  } catch (error) {
    console.error('获取订单历史失败:', error)
  }
}

const loadFavoriteItems = async () => {
  try {
    // 模拟收藏商品数据
    const response = await menuAPI.getPopularItems({ limit: 6 })
    favoriteItems.value = response.data || []
  } catch (error) {
    console.error('获取收藏商品失败:', error)
  }
}

const loadAddresses = async () => {
  try {
    // 模拟地址数据
    addresses.value = [
      {
        id: 1,
        contact_name: '张三',
        phone: '13800138000',
        full_address: '北京市朝阳区建国门外大街1号',
        is_default: true
      }
    ]
  } catch (error) {
    console.error('获取收货地址失败:', error)
  }
}

const beforeAvatarUpload = (file) => {
  const isJPG = file.type === 'image/jpeg' || file.type === 'image/png'
  const isLt2M = file.size / 1024 / 1024 < 2

  if (!isJPG) {
    ElMessage.error('上传头像图片只能是 JPG/PNG 格式!')
  }
  if (!isLt2M) {
    ElMessage.error('上传头像图片大小不能超过 2MB!')
  }
  return isJPG && isLt2M
}

const handleAvatarUpload = async (options) => {
  try {
    // 这里应该调用上传API
    ElMessage.success('头像上传成功')
  } catch (error) {
    ElMessage.error('头像上传失败')
  }
}

const saveProfile = async () => {
  savingProfile.value = true

  try {
    await authAPI.updateUserProfile(editForm)
    await loadUserInfo()
    ElMessage.success('个人资料保存成功')
    editProfileVisible.value = false
  } catch (error) {
    console.error('保存个人资料失败:', error)
    ElMessage.error('保存失败，请稍后重试')
  } finally {
    savingProfile.value = false
  }
}

const changePassword = async () => {
  changingPassword.value = true

  try {
    await authAPI.changePassword(passwordForm)
    ElMessage.success('密码修改成功')
    changePasswordVisible.value = false

    // 重置表单
    Object.keys(passwordForm).forEach(key => {
      passwordForm[key] = ''
    })
  } catch (error) {
    console.error('修改密码失败:', error)
    ElMessage.error('修改密码失败，请稍后重试')
  } finally {
    changingPassword.value = false
  }
}

const handleAddToCart = async (item, quantity = 1) => {
  try {
    await cartStore.addItem(item, quantity)
    ElMessage.success(`${item.name} 已添加到购物车`)
  } catch (error) {
    console.error('添加到购物车失败:', error)
    ElMessage.error('添加到购物车失败，请稍后重试')
  }
}

const handleRemoveFavorite = async (item) => {
  try {
    // 调用取消收藏API
    ElMessage.success(`${item.name} 已取消收藏`)
  } catch (error) {
    ElMessage.error('取消收藏失败')
  }
}

const viewOrderDetail = (order) => {
  router.push(`/orders/${order.id}`)
}

const goToOrders = () => {
  router.push('/orders')
}

const goToMenu = () => {
  router.push('/menu')
}

const getTabTitle = (tab) => {
  const titles = {
    settings: '偏好设置',
    notifications: '消息通知'
  }
  return titles[tab] || '功能页面'
}

const editAddress = (address) => {
  // 编辑地址逻辑
  ElMessage.info('编辑地址功能开发中')
}

const setDefaultAddress = async (address) => {
  try {
    // 设置默认地址API调用
    ElMessage.success('已设置默认地址')
    await loadAddresses()
  } catch (error) {
    ElMessage.error('设置默认地址失败')
  }
}

const deleteAddress = async (address) => {
  try {
    await ElMessageBox.confirm(
      '确定要删除这个地址吗？',
      '确认删除',
      { type: 'warning' }
    )

    // 删除地址API调用
    ElMessage.success('地址已删除')
    await loadAddresses()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除地址失败')
    }
  }
}

// 生命周期
onMounted(async () => {
  await Promise.all([
    loadUserInfo(),
    loadUserStats(),
    loadRecentOrders()
  ])
})
</script>

<style lang="scss" scoped>
.profile-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 100px 20px 40px;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;

  .header-content {
    max-width: 800px;
    margin: 0 auto;
  }

  .page-title {
    font-size: 2.5rem;
    font-weight: bold;
    color: #2c3e50;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 15px;

    .title-icon {
      font-size: 2.2rem;
      color: #8b4513;
    }
  }

  .page-subtitle {
    font-size: 1.1rem;
    color: #7f8c8d;
    margin: 0;
  }
}

.profile-container {
  max-width: 1200px;
  margin: 0 auto;
}

.profile-sidebar {
  .user-card,
  .nav-card {
    margin-bottom: 24px;
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

    :deep(.el-card__body) {
      padding: 24px;
    }
  }

  .user-info {
    text-align: center;

    .avatar-section {
      position: relative;
      margin-bottom: 20px;

      .avatar-uploader {
        :deep(.el-upload) {
          border: 1px dashed #d9d9d9;
          border-radius: 50%;
          cursor: pointer;
          position: relative;
          overflow: hidden;
          transition: all 0.3s ease;

          &:hover {
            border-color: #8b4513;
          }
        }

        .avatar {
          width: 100px;
          height: 100px;
          border-radius: 50%;
          object-fit: cover;
        }

        .avatar-uploader-icon {
          font-size: 28px;
          color: #8c939d;
          width: 100px;
          height: 100px;
          line-height: 100px;
          text-align: center;
        }
      }

      .avatar-status {
        position: absolute;
        bottom: 5px;
        right: 5px;
      }
    }

    .user-details {
      .user-name {
        margin: 0 0 8px 0;
        font-size: 1.5rem;
        color: #2c3e50;
        font-weight: bold;
      }

      .user-email {
        color: #7f8c8d;
        margin-bottom: 12px;
      }

      .user-meta {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 12px;
        font-size: 0.9rem;
        color: #95a5a6;
      }
    }

    .user-actions {
      margin-top: 20px;
      display: flex;
      flex-direction: column;
      gap: 12px;

      .edit-btn,
      .password-btn {
        border-radius: 20px;
        transition: all 0.3s ease;

        &:hover {
          transform: translateY(-2px);
        }
      }
    }
  }

  .profile-menu {
    border: none;

    :deep(.el-menu-item) {
      margin-bottom: 8px;
      border-radius: 8px;
      transition: all 0.3s ease;

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

.profile-content {
  .content-section {
    margin-bottom: 24px;
  }

  .overview-card,
  .orders-card,
  .favorites-card,
  .addresses-card {
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

    :deep(.el-card__header) {
      border-bottom: 1px solid #f0f0f0;

      h3 {
        margin: 0;
        color: #2c3e50;
        font-size: 1.2rem;
      }

      .card-header {
        display: flex;
        justify-content: space-between;
        align-items: center;

        .view-all-btn,
        .add-btn {
          border-radius: 20px;
        }
      }
    }
  }

  .stat-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px;
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);
    border-radius: 12px;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-3px);
      box-shadow: 0 6px 20px rgba(0, 0, 0, 0.1);
    }

    .stat-icon {
      width: 50px;
      height: 50px;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 1.5rem;
      background: linear-gradient(135deg, #8b4513, #a0522d);
      color: white;
    }

    .stat-info {
      flex: 1;

      .stat-value {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        line-height: 1;
        margin-bottom: 4px;
      }

      .stat-label {
        font-size: 0.9rem;
        color: #7f8c8d;
      }
    }
  }

  .recent-orders {
    margin-top: 30px;

    h4 {
      margin: 0 0 16px 0;
      color: #2c3e50;
      font-size: 1.1rem;
    }

    .order-list {
      .order-item {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 12px 16px;
        background: #f8f9fa;
        border-radius: 8px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.3s ease;

        &:hover {
          background: #e9ecef;
          transform: translateX(5px);
        }

        .order-info {
          display: flex;
          flex-direction: column;
          gap: 4px;

          .order-number {
            font-weight: 500;
            color: #2c3e50;
          }

          .order-time {
            font-size: 0.85rem;
            color: #7f8c8d;
          }
        }

        .order-amount {
          font-weight: bold;
          color: #e74c3c;
          margin-right: 12px;
        }
      }
    }
  }

  .orders-content {
    .empty-orders {
      padding: 60px 20px;
      text-align: center;
    }

    .order-history-list {
      .order-history-item {
        border: 1px solid #e0e0e0;
        border-radius: 8px;
        padding: 16px;
        margin-bottom: 12px;
        transition: all 0.3s ease;

        &:hover {
          box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        }

        .order-header {
          display: flex;
          justify-content: space-between;
          align-items: center;
          margin-bottom: 12px;
        }

        .order-content {
          display: flex;
          justify-content: space-between;
          align-items: center;

          .order-items-preview {
            display: flex;
            align-items: center;
            gap: 8px;

            .item-preview {
              width: 30px;
              height: 30px;
              border-radius: 4px;
              object-fit: cover;
            }

            .more-items {
              font-size: 0.85rem;
              color: #7f8c8d;
            }
          }

          .order-details {
            display: flex;
            flex-direction: column;
            align-items: flex-end;
            gap: 4px;

            .order-time {
              font-size: 0.85rem;
              color: #7f8c8d;
            }

            .order-amount {
              font-weight: bold;
              color: #e74c3c;
            }
          }
        }
      }
    }
  }

  .empty-favorites,
  .empty-addresses {
    padding: 60px 20px;
    text-align: center;
  }

  .favorites-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 16px;
  }

  .addresses-list {
    .address-item {
      border: 1px solid #e0e0e0;
      border-radius: 8px;
      padding: 16px;
      margin-bottom: 12px;
      transition: all 0.3s ease;

      &.default-address {
        border-color: #27ae60;
        background: rgba(39, 174, 96, 0.05);
      }

      &:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
      }

      .address-content {
        margin-bottom: 12px;

        .address-header {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 8px;

          .contact-name {
            font-weight: bold;
            color: #2c3e50;
          }

          .contact-phone {
            color: #7f8c8d;
          }
        }

        .address-detail {
          color: #7f8c8d;
          line-height: 1.5;
        }
      }

      .address-actions {
        display: flex;
        gap: 16px;

        .delete-btn {
          color: #e74c3c;

          &:hover {
            background: rgba(231, 76, 60, 0.1);
          }
        }
      }
    }
  }

  .placeholder-content {
    padding: 60px 20px;
    text-align: center;
  }
}

// 弹窗样式
.profile-dialog,
.password-dialog {
  :deep(.el-dialog) {
    border-radius: 12px;
  }
}

// 响应式设计
@media (max-width: 768px) {
  .profile-page {
    padding: 80px 16px 32px;
  }

  .page-title {
    font-size: 2rem !important;

    .title-icon {
      font-size: 1.8rem !important;
    }
  }

  .user-info {
    .user-details {
      .user-name {
        font-size: 1.3rem;
      }

      .user-meta {
        flex-direction: column;
        gap: 8px;
      }
    }

    .user-actions {
      flex-direction: row;
      justify-content: center;

      .edit-btn,
      .password-btn {
        flex: 1;
        max-width: 120px;
      }
    }
  }

  .stat-item {
    padding: 16px;

    .stat-icon {
      width: 40px;
      height: 40px;
      font-size: 1.2rem;
    }

    .stat-info {
      .stat-value {
        font-size: 1.3rem;
      }
    }
  }

  .favorites-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
  }

  .order-history-item {
    .order-content {
      flex-direction: column;
      align-items: stretch;
      gap: 12px;

      .order-items-preview {
        justify-content: flex-start;
      }

      .order-details {
        align-items: flex-start;
      }
    }
  }
}

@media (max-width: 480px) {
  .profile-page {
    padding: 70px 12px 24px;
  }

  .page-title {
    font-size: 1.8rem !important;
    flex-direction: column;
    gap: 8px;

    .title-icon {
      font-size: 1.6rem !important;
    }
  }

  .stat-item {
    flex-direction: column;
    text-align: center;
    gap: 12px;
  }

  .favorites-grid {
    grid-template-columns: 1fr;
  }
}
</style>