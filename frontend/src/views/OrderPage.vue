<template>
  <div class="order-page">
    <!-- 页面头部 -->
    <div class="page-header animate__animated animate__fadeInDown">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><List /></el-icon>
          我的订单
        </h1>
        <p class="page-subtitle">查看和管理您的订单信息</p>
      </div>
    </div>

    <div class="order-container">
      <!-- 筛选和搜索区域 -->
      <div class="filter-section animate__animated animate__fadeInUp">
        <el-card class="filter-card" shadow="hover">
          <div class="filter-content">
            <!-- 订单状态筛选 -->
            <div class="status-filter">
              <el-radio-group v-model="selectedStatus" @change="handleStatusChange">
                <el-radio-button
                  v-for="status in statusOptions"
                  :key="status.value"
                  :label="status.value"
                >
                  <el-icon v-if="status.icon">
                    <component :is="status.icon" />
                  </el-icon>
                  {{ status.label }}
                </el-radio-button>
              </el-radio-group>
            </div>

            <!-- 时间范围筛选 -->
            <div class="date-filter">
              <el-date-picker
                v-model="dateRange"
                type="daterange"
                range-separator="至"
                start-placeholder="开始日期"
                end-placeholder="结束日期"
                format="YYYY-MM-DD"
                value-format="YYYY-MM-DD"
                @change="handleDateChange"
                class="date-picker"
              />
            </div>

            <!-- 搜索框 -->
            <div class="search-box">
              <el-input
                v-model="searchQuery"
                placeholder="搜索订单号或商品名称..."
                prefix-icon="Search"
                clearable
                @input="handleSearch"
                class="search-input"
              />
            </div>

            <!-- 刷新按钮 -->
            <el-button
              :icon="Refresh"
              @click="refreshOrders"
              :loading="loading"
              class="refresh-btn"
            >
              刷新
            </el-button>
          </div>
        </el-card>
      </div>

      <!-- 订单统计 -->
      <div v-if="statistics" class="statistics-section animate__animated animate__fadeInUp">
        <el-row :gutter="20">
          <el-col :xs="12" :sm="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon">
                  <el-icon><ShoppingCart /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.total_orders || 0 }}</div>
                  <div class="stat-label">总订单</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="12" :sm="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon pending">
                  <el-icon><Clock /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.pending_orders || 0 }}</div>
                  <div class="stat-label">待处理</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="12" :sm="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon completed">
                  <el-icon><CircleCheck /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">{{ statistics.completed_orders || 0 }}</div>
                  <div class="stat-label">已完成</div>
                </div>
              </div>
            </el-card>
          </el-col>
          <el-col :xs="12" :sm="6">
            <el-card class="stat-card">
              <div class="stat-content">
                <div class="stat-icon total">
                  <el-icon><Money /></el-icon>
                </div>
                <div class="stat-info">
                  <div class="stat-value">¥{{ (statistics.total_amount || 0).toFixed(2) }}</div>
                  <div class="stat-label">总消费</div>
                </div>
              </div>
            </el-card>
          </el-col>
        </el-row>
      </div>

      <!-- 订单列表 -->
      <div class="orders-section">
        <el-card class="orders-card animate__animated animate__fadeInLeft">
          <template #header>
            <div class="card-header">
              <h3>订单列表 ({{ totalCount || 0 }})</h3>
              <div class="header-actions">
                <el-select
                  v-model="sortBy"
                  placeholder="排序方式"
                  @change="handleSortChange"
                  class="sort-select"
                >
                  <el-option label="最新订单" value="created_at_desc" />
                  <el-option label="最早订单" value="created_at_asc" />
                  <el-option label="金额从高到低" value="amount_desc" />
                  <el-option label="金额从低到高" value="amount_asc" />
                </el-select>
              </div>
            </div>
          </template>

          <!-- 加载状态 -->
          <div v-if="loading" class="loading-container">
            <el-skeleton :rows="5" animated />
          </div>

          <!-- 空状态 -->
          <div v-else-if="orders.length === 0" class="empty-orders">
            <el-empty description="暂无订单">
              <template #image>
                <el-icon size="80"><Document /></el-icon>
              </template>
              <el-button type="primary" @click="goToMenu">
                去点餐
              </el-button>
            </el-empty>
          </div>

          <!-- 订单列表 -->
          <div v-else class="orders-list">
            <div
              v-for="order in orders"
              :key="order.id"
              class="order-item animate__animated animate__fadeInUp"
              :style="{ 'animation-delay': `${getItemAnimationDelay(order.id)}ms` }"
            >
              <!-- 订单头部 -->
              <div class="order-header">
                <div class="order-info">
                  <div class="order-number">
                    订单号: {{ order.order_number }}
                  </div>
                  <div class="order-time">
                    {{ formatDateTime(order.created_at) }}
                  </div>
                </div>
                <div class="order-status">
                  <el-tag
                    :type="getStatusType(order.status)"
                    :icon="getStatusIcon(order.status)"
                  >
                    {{ getStatusLabel(order.status) }}
                  </el-tag>
                </div>
              </div>

              <!-- 订单商品 -->
              <div class="order-items">
                <div
                  v-for="item in order.items.slice(0, 3)"
                  :key="item.id"
                  class="order-item-preview"
                >
                  <img
                    :src="item.image_url || '/default-coffee.jpg'"
                    :alt="item.name"
                    class="item-image"
                    @error="handleImageError"
                  />
                  <div class="item-info">
                    <h5 class="item-name">{{ item.name }}</h5>
                    <p class="item-details">
                      ¥{{ item.price }} x {{ item.quantity }}
                    </p>
                  </div>
                </div>

                <!-- 更多商品提示 -->
                <div
                  v-if="order.items.length > 3"
                  class="more-items"
                >
                  <el-icon><More /></el-icon>
                  <span>还有{{ order.items.length - 3 }}件商品</span>
                </div>
              </div>

              <!-- 订单底部 -->
              <div class="order-footer">
                <div class="order-total">
                  <span class="total-label">订单金额:</span>
                  <span class="total-amount">¥{{ order.total_price.toFixed(2) }}</span>
                </div>
                <div class="order-actions">
                  <el-button
                    type="text"
                    @click="viewOrderDetail(order)"
                    class="detail-btn"
                  >
                    查看详情
                  </el-button>
                  <el-button
                    v-if="order.status === 'pending'"
                    type="warning"
                    @click="cancelOrder(order)"
                    class="cancel-btn"
                  >
                    取消订单
                  </el-button>
                  <el-button
                    v-if="order.status === 'completed'"
                    type="primary"
                    @click="reorder(order)"
                    class="reorder-btn"
                  >
                    再来一单
                  </el-button>
                </div>
              </div>
            </div>
          </div>

          <!-- 分页 -->
          <div v-if="orders.length > 0" class="pagination-section">
            <el-pagination
              v-model:current-page="currentPage"
              v-model:page-size="pageSize"
              :page-sizes="[10, 20, 50]"
              :total="totalCount"
              layout="total, sizes, prev, pager, next, jumper"
              @size-change="handleSizeChange"
              @current-change="handleCurrentChange"
            />
          </div>
        </el-card>
      </div>
    </div>

    <!-- 订单详情弹窗 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="`订单详情 - ${selectedOrder?.order_number}`"
      width="800px"
      class="order-detail-dialog"
      destroy-on-close
    >
      <div v-if="selectedOrder" class="order-detail">
        <!-- 订单基本信息 -->
        <div class="detail-section">
          <h4 class="section-title">订单信息</h4>
          <el-descriptions :column="2" border>
            <el-descriptions-item label="订单号">
              {{ selectedOrder.order_number }}
            </el-descriptions-item>
            <el-descriptions-item label="订单状态">
              <el-tag
                :type="getStatusType(selectedOrder.status)"
                :icon="getStatusIcon(selectedOrder.status)"
              >
                {{ getStatusLabel(selectedOrder.status) }}
              </el-tag>
            </el-descriptions-item>
            <el-descriptions-item label="下单时间">
              {{ formatDateTime(selectedOrder.created_at) }}
            </el-descriptions-item>
            <el-descriptions-item label="支付方式">
              {{ selectedOrder.payment_method || '在线支付' }}
            </el-descriptions-item>
            <el-descriptions-item label="配送地址" :span="2">
              {{ selectedOrder.delivery_address || '到店自取' }}
            </el-descriptions-item>
            <el-descriptions-item label="备注" :span="2">
              {{ selectedOrder.remark || '无' }}
            </el-descriptions-item>
          </el-descriptions>
        </div>

        <!-- 商品明细 -->
        <div class="detail-section">
          <h4 class="section-title">商品明细</h4>
          <el-table :data="selectedOrder.items" stripe>
            <el-table-column prop="name" label="商品名称" min-width="200" />
            <el-table-column prop="price" label="单价" width="100">
              <template #default="{ row }">
                ¥{{ row.price.toFixed(2) }}
              </template>
            </el-table-column>
            <el-table-column prop="quantity" label="数量" width="80" />
            <el-table-column label="小计" width="100">
              <template #default="{ row }">
                ¥{{ (row.price * row.quantity).toFixed(2) }}
              </template>
            </el-table-column>
          </el-table>
        </div>

        <!-- 费用明细 -->
        <div class="detail-section">
          <h4 class="section-title">费用明细</h4>
          <div class="cost-details">
            <div class="cost-row">
              <span>商品总价</span>
              <span>¥{{ selectedOrder.subtotal_price?.toFixed(2) || '0.00' }}</span>
            </div>
            <div class="cost-row" v-if="selectedOrder.delivery_fee > 0">
              <span>配送费</span>
              <span>¥{{ selectedOrder.delivery_fee.toFixed(2) }}</span>
            </div>
            <div class="cost-row" v-if="selectedOrder.discount > 0">
              <span>优惠金额</span>
              <span class="discount">-¥{{ selectedOrder.discount.toFixed(2) }}</span>
            </div>
            <div class="cost-divider"></div>
            <div class="cost-row total">
              <span>订单总额</span>
              <span class="total-amount">¥{{ selectedOrder.total_price.toFixed(2) }}</span>
            </div>
          </div>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">关闭</el-button>
          <el-button
            v-if="selectedOrder?.status === 'pending'"
            type="warning"
            @click="cancelOrderFromDetail"
          >
            取消订单
          </el-button>
          <el-button
            v-if="selectedOrder?.status === 'completed'"
            type="primary"
            @click="reorderFromDetail"
          >
            再来一单
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  List,
  ShoppingCart,
  Clock,
  CircleCheck,
  Money,
  Document,
  Refresh,
  Search,
  More,
  Timer,
  SuccessFilled,
  Warning,
  CircleClose
} from '@element-plus/icons-vue'
import orderAPI from '@/api/order'
import { useCartStore } from '@/store/cart'

// 路由和状态管理
const router = useRouter()
const cartStore = useCartStore()

// 响应式数据
const loading = ref(false)
const orders = ref([])
const statistics = ref(null)
const totalCount = ref(0)
const currentPage = ref(1)
const pageSize = ref(10)
const selectedStatus = ref('all')
const dateRange = ref([])
const searchQuery = ref('')
const sortBy = ref('created_at_desc')
const detailDialogVisible = ref(false)
const selectedOrder = ref(null)

// 订单状态选项
const statusOptions = [
  { value: 'all', label: '全部', icon: List },
  { value: 'pending', label: '待处理', icon: Timer },
  { value: 'processing', label: '处理中', icon: Clock },
  { value: 'delivering', label: '配送中', icon: ShoppingCart },
  { value: 'completed', label: '已完成', icon: SuccessFilled },
  { value: 'cancelled', label: '已取消', icon: CircleClose }
]

// 分页数据
const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
})

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

const getStatusIcon = (status) => {
  const iconMap = {
    'pending': Timer,
    'processing': Clock,
    'delivering': ShoppingCart,
    'completed': SuccessFilled,
    'cancelled': CircleClose
  }
  return iconMap[status] || List
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
const formatDateTime = (dateTime) => {
  if (!dateTime) return '-'
  return new Date(dateTime).toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

const getItemAnimationDelay = (orderId) => {
  const index = orders.value.findIndex(order => order.id === orderId)
  return index * 50
}

const handleImageError = (event) => {
  event.target.src = '/default-coffee.jpg'
}

const getOrders = async (reset = false) => {
  if (reset) {
    currentPage.value = 1
    orders.value = []
  }

  loading.value = true

  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value,
      status: selectedStatus.value === 'all' ? undefined : selectedStatus.value,
      start_date: dateRange.value?.[0],
      end_date: dateRange.value?.[1],
      search: searchQuery.value || undefined,
      sort: sortBy.value
    }

    const response = await orderAPI.getMyOrders(params)

    if (reset) {
      orders.value = response.data.items || []
    } else {
      orders.value.push(...(response.data.items || []))
    }

    totalCount.value = response.data.total || 0
    pagination.total = totalCount.value

  } catch (error) {
    console.error('获取订单列表失败:', error)
    ElMessage.error('获取订单列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const getStatistics = async () => {
  try {
    const response = await orderAPI.getOrderStatistics()
    statistics.value = response.data
  } catch (error) {
    console.error('获取订单统计失败:', error)
  }
}

const handleStatusChange = () => {
  getOrders(true)
}

const handleDateChange = () => {
  getOrders(true)
}

const handleSearch = () => {
  // 防抖处理
  clearTimeout(handleSearch.debounceTimer)
  handleSearch.debounceTimer = setTimeout(() => {
    getOrders(true)
  }, 500)
}

const handleSortChange = () => {
  getOrders(true)
}

const handleSizeChange = (size) => {
  pageSize.value = size
  getOrders(true)
}

const handleCurrentChange = (page) => {
  currentPage.value = page
  getOrders()
}

const refreshOrders = () => {
  getOrders(true)
  getStatistics()
}

const viewOrderDetail = (order) => {
  selectedOrder.value = order
  detailDialogVisible.value = true
}

const cancelOrder = async (order) => {
  try {
    await ElMessageBox.confirm(
      `确定要取消订单 ${order.order_number} 吗？`,
      '确认取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await orderAPI.cancelOrder(order.id)
    ElMessage.success('订单已取消')
    getOrders(true)
    getStatistics()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消订单失败:', error)
      ElMessage.error('取消订单失败，请稍后重试')
    }
  }
}

const cancelOrderFromDetail = async () => {
  if (!selectedOrder.value) return

  try {
    await ElMessageBox.confirm(
      `确定要取消订单 ${selectedOrder.value.order_number} 吗？`,
      '确认取消',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await orderAPI.cancelOrder(selectedOrder.value.id)
    ElMessage.success('订单已取消')
    detailDialogVisible.value = false
    getOrders(true)
    getStatistics()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('取消订单失败:', error)
      ElMessage.error('取消订单失败，请稍后重试')
    }
  }
}

const reorder = async (order) => {
  try {
    // 将订单商品添加到购物车
    for (const item of order.items) {
      await cartStore.addItem({
        id: item.menu_id,
        name: item.name,
        price: item.price,
        image_url: item.image_url
      }, item.quantity)
    }

    ElMessage.success('商品已添加到购物车')
    router.push('/cart')
  } catch (error) {
    console.error('重新下单失败:', error)
    ElMessage.error('重新下单失败，请稍后重试')
  }
}

const reorderFromDetail = async () => {
  if (!selectedOrder.value) return

  await reorder(selectedOrder.value)
  detailDialogVisible.value = false
}

const goToMenu = () => {
  router.push('/menu')
}

// 生命周期
onMounted(async () => {
  await Promise.all([
    getOrders(true),
    getStatistics()
  ])
})
</script>

<style lang="scss" scoped>
.order-page {
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

.order-container {
  max-width: 1200px;
  margin: 0 auto;
}

.filter-section {
  margin-bottom: 24px;

  .filter-card {
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  }

  .filter-content {
    display: flex;
    flex-wrap: wrap;
    gap: 20px;
    align-items: center;
    padding: 10px 0;

    .status-filter {
      flex: 1;
      min-width: 300px;

      :deep(.el-radio-group) {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }
    }

    .date-filter {
      min-width: 240px;

      .date-picker {
        width: 100%;
      }
    }

    .search-box {
      flex: 1;
      min-width: 250px;

      .search-input {
        max-width: 300px;
      }
    }

    .refresh-btn {
      color: #8b4513;
      border-color: #8b4513;

      &:hover {
        background: rgba(139, 69, 19, 0.1);
      }
    }
  }
}

.statistics-section {
  margin-bottom: 24px;

  .stat-card {
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-5px);
      box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    }

    :deep(.el-card__body) {
      padding: 20px;
    }

    .stat-content {
      display: flex;
      align-items: center;
      gap: 16px;

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

        &.pending {
          background: linear-gradient(135deg, #f39c12, #e67e22);
        }

        &.completed {
          background: linear-gradient(135deg, #27ae60, #2ecc71);
        }

        &.total {
          background: linear-gradient(135deg, #e74c3c, #c0392b);
        }
      }

      .stat-info {
        flex: 1;

        .stat-value {
          font-size: 1.8rem;
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
  }
}

.orders-section {
  .orders-card {
    border-radius: 12px;
    border: none;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

    .card-header {
      display: flex;
      justify-content: space-between;
      align-items: center;

      h3 {
        margin: 0;
        color: #2c3e50;
        font-size: 1.2rem;
      }

      .sort-select {
        width: 150px;
      }
    }
  }

  .loading-container {
    padding: 40px;
  }

  .empty-orders {
    padding: 60px 20px;
    text-align: center;
  }

  .orders-list {
    .order-item {
      border: 1px solid #e0e0e0;
      border-radius: 12px;
      padding: 20px;
      margin-bottom: 16px;
      background: white;
      transition: all 0.3s ease;

      &:hover {
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
        transform: translateY(-2px);
      }

      .order-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 16px;
        padding-bottom: 12px;
        border-bottom: 1px solid #f0f0f0;

        .order-info {
          .order-number {
            font-size: 1.1rem;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 4px;
          }

          .order-time {
            font-size: 0.9rem;
            color: #7f8c8d;
          }
        }
      }

      .order-items {
        display: flex;
        align-items: center;
        gap: 16px;
        margin-bottom: 16px;

        .order-item-preview {
          display: flex;
          align-items: center;
          gap: 12px;
          flex: 1;
          min-width: 0;

          .item-image {
            width: 50px;
            height: 50px;
            border-radius: 8px;
            object-fit: cover;
            flex-shrink: 0;
          }

          .item-info {
            flex: 1;
            min-width: 0;

            .item-name {
              margin: 0 0 4px 0;
              font-size: 0.95rem;
              color: #2c3e50;
              font-weight: 500;
              white-space: nowrap;
              overflow: hidden;
              text-overflow: ellipsis;
            }

            .item-details {
              margin: 0;
              font-size: 0.85rem;
              color: #7f8c8d;
            }
          }
        }

        .more-items {
          display: flex;
          align-items: center;
          gap: 4px;
          color: #7f8c8d;
          font-size: 0.85rem;
          flex-shrink: 0;
        }
      }

      .order-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding-top: 12px;
        border-top: 1px solid #f0f0f0;

        .order-total {
          .total-label {
            color: #7f8c8d;
            margin-right: 8px;
          }

          .total-amount {
            font-size: 1.2rem;
            font-weight: bold;
            color: #e74c3c;
          }
        }

        .order-actions {
          display: flex;
          gap: 12px;

          .detail-btn,
          .cancel-btn,
          .reorder-btn {
            border-radius: 20px;
            transition: all 0.3s ease;

            &:hover {
              transform: translateY(-2px);
            }
          }
        }
      }
    }
  }

  .pagination-section {
    margin-top: 24px;
    text-align: center;
  }
}

// 订单详情弹窗
.order-detail-dialog {
  :deep(.el-dialog) {
    border-radius: 12px;
  }

  .order-detail {
    .detail-section {
      margin-bottom: 24px;

      &:last-child {
        margin-bottom: 0;
      }

      .section-title {
        margin: 0 0 16px 0;
        color: #2c3e50;
        font-size: 1.1rem;
        font-weight: 600;
      }
    }

    .cost-details {
      .cost-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 8px;

        &.discount {
          color: #27ae60;
        }

        &.total {
          font-weight: bold;
          font-size: 1.1rem;
          color: #2c3e50;

          .total-amount {
            color: #e74c3c;
            font-size: 1.3rem;
          }
        }
      }

      .cost-divider {
        height: 1px;
        background: #e0e0e0;
        margin: 12px 0;
      }
    }
  }

  .dialog-footer {
    .el-button {
      border-radius: 20px;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .order-page {
    padding: 80px 16px 32px;
  }

  .page-title {
    font-size: 2rem !important;

    .title-icon {
      font-size: 1.8rem !important;
    }
  }

  .filter-content {
    flex-direction: column;
    align-items: stretch;

    .status-filter,
    .date-filter,
    .search-box {
      width: 100%;
      min-width: auto;
    }

    .search-input {
      max-width: none;
    }
  }

  .statistics-section {
    .stat-card {
      margin-bottom: 16px;

      .stat-content {
        .stat-icon {
          width: 40px;
          height: 40px;
          font-size: 1.2rem;
        }

        .stat-info {
          .stat-value {
            font-size: 1.5rem;
          }
        }
      }
    }
  }

  .orders-card {
    .card-header {
      flex-direction: column;
      align-items: stretch;
      gap: 16px;

      .sort-select {
        width: 100%;
      }
    }
  }

  .order-item {
    .order-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;
    }

    .order-items {
      flex-direction: column;
      align-items: stretch;
      gap: 12px;

      .order-item-preview {
        .item-image {
          width: 40px;
          height: 40px;
        }
      }
    }

    .order-footer {
      flex-direction: column;
      align-items: stretch;
      gap: 12px;

      .order-actions {
        justify-content: center;
      }
    }
  }
}

@media (max-width: 480px) {
  .order-page {
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

  .status-filter {
    :deep(.el-radio-group) {
      .el-radio-button {
        margin-bottom: 8px;
      }
    }
  }
}
</style>