<template>
  <div class="cart-page">
    <!-- 页面头部 -->
    <div class="page-header animate__animated animate__fadeInDown">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><ShoppingCart /></el-icon>
          购物车
        </h1>
        <p class="page-subtitle">确认您选择的商品</p>
      </div>
    </div>

    <div class="cart-container">
      <el-row :gutter="24">
        <!-- 左侧：购物车商品列表 -->
        <el-col :xs="24" :lg="16">
          <el-card class="cart-card animate__animated animate__fadeInLeft">
            <template #header>
              <div class="card-header">
                <h3>商品列表 ({{ cartItemsCount }})</h3>
                <el-button
                  v-if="cartItemsCount > 0"
                  type="text"
                  @click="clearCart"
                  class="clear-btn"
                >
                  <el-icon><Delete /></el-icon>
                  清空购物车
                </el-button>
              </div>
            </template>

            <!-- 购物车为空 -->
            <div v-if="cartItemsCount === 0" class="empty-cart">
              <el-empty description="购物车是空的">
                <template #image>
                  <el-icon size="80"><ShoppingCart /></el-icon>
                </template>
                <el-button type="primary" @click="goToMenu">
                  去选购商品
                </el-button>
              </el-empty>
            </div>

            <!-- 购物车商品列表 -->
            <div v-else class="cart-items">
              <div
                v-for="item in cartItems"
                :key="item.id"
                class="cart-item animate__animated animate__fadeInUp"
                :style="{ 'animation-delay': `${getItemAnimationDelay(item.id)}ms` }"
              >
                <!-- 商品图片 -->
                <div class="item-image">
                  <img
                    :src="item.image_url || '/default-coffee.jpg'"
                    :alt="item.name"
                    @error="handleImageError"
                  />
                </div>

                <!-- 商品信息 -->
                <div class="item-info">
                  <h4 class="item-name">{{ item.name }}</h4>
                  <p class="item-description">{{ item.description }}</p>
                  <div class="item-tags" v-if="item.tags && item.tags.length > 0">
                    <el-tag
                      v-for="tag in item.tags.slice(0, 2)"
                      :key="tag"
                      size="small"
                      effect="light"
                    >
                      {{ tag }}
                    </el-tag>
                  </div>
                </div>

                <!-- 价格信息 -->
                <div class="item-price">
                  <div class="price-info">
                    <span class="current-price">¥{{ item.price }}</span>
                    <span
                      v-if="item.original_price && item.original_price > item.price"
                      class="original-price"
                    >
                      ¥{{ item.original_price }}
                    </span>
                  </div>
                  <div class="item-subtotal">
                    小计: ¥{{ (item.price * item.quantity).toFixed(2) }}
                  </div>
                </div>

                <!-- 数量控制 -->
                <div class="item-quantity">
                  <el-input-number
                    :model-value="item.quantity"
                    :min="1"
                    :max="99"
                    size="large"
                    @change="handleQuantityChange(item, $event)"
                  />
                </div>

                <!-- 操作按钮 -->
                <div class="item-actions">
                  <el-button
                    type="text"
                    :icon="Delete"
                    @click="handleRemoveItem(item)"
                    class="remove-btn"
                  >
                    移除
                  </el-button>
                </div>
              </div>
            </div>
          </el-card>

          <!-- 推荐商品 -->
          <el-card
            v-if="recommendations.length > 0"
            class="recommendations-card animate__animated animate__fadeInUp"
          >
            <template #header>
              <h3>为您推荐</h3>
            </template>
            <div class="recommendations-grid">
              <div
                v-for="item in recommendations"
                :key="item.id"
                class="recommendation-item"
              >
                <CoffeeCard
                  :item="item"
                  :show-quick-actions="false"
                  @add-to-cart="handleAddToCart"
                />
              </div>
            </div>
          </el-card>
        </el-col>

        <!-- 右侧：订单汇总 -->
        <el-col :xs="24" :lg="8">
          <div class="order-summary animate__animated animate__fadeInRight">
            <!-- 订单信息卡片 -->
            <el-card class="summary-card">
              <template #header>
                <h3>订单汇总</h3>
              </template>

              <div class="summary-content">
                <!-- 优惠码输入 -->
                <div class="coupon-section">
                  <el-input
                    v-model="couponCode"
                    placeholder="输入优惠码"
                    clearable
                  >
                    <template #append>
                      <el-button
                        type="primary"
                        :disabled="!couponCode.trim()"
                        @click="applyCoupon"
                        :loading="applyingCoupon"
                      >
                        应用
                      </el-button>
                    </template>
                  </el-input>
                </div>

                <!-- 价格明细 -->
                <div class="price-details">
                  <div class="price-row">
                    <span>商品总价</span>
                    <span>¥{{ subtotal.toFixed(2) }}</span>
                  </div>
                  <div class="price-row" v-if="discount > 0">
                    <span>优惠金额</span>
                    <span class="discount">-¥{{ discount.toFixed(2) }}</span>
                  </div>
                  <div class="price-row">
                    <span>配送费</span>
                    <span>{{ deliveryFee === 0 ? '免费' : `¥${deliveryFee.toFixed(2)}` }}</span>
                  </div>
                  <div class="price-divider"></div>
                  <div class="price-row total">
                    <span>总计</span>
                    <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
                  </div>
                </div>

                <!-- 配送信息 -->
                <div class="delivery-info" v-if="cartItemsCount > 0">
                  <el-alert
                    title="满￥30免配送费"
                    type="success"
                    :closable="false"
                    show-icon
                    v-if="deliveryFee === 0"
                  />
                  <el-alert
                    :title="`还差￥${(30 - subtotal).toFixed(2)}免配送费`"
                    type="info"
                    :closable="false"
                    show-icon
                    v-else
                  />
                </div>

                <!-- 结算按钮 -->
                <div class="checkout-section">
                  <el-button
                    type="primary"
                    size="large"
                    :disabled="cartItemsCount === 0"
                    @click="handleCheckout"
                    class="checkout-btn"
                  >
                    <el-icon><CreditCard /></el-icon>
                    去结算 ({{ cartItemsCount }})
                  </el-button>
                </div>
              </div>
            </el-card>

            <!-- 配送说明卡片 -->
            <el-card class="delivery-card">
              <template #header>
                <h3>配送说明</h3>
              </template>
              <div class="delivery-content">
                <div class="delivery-item">
                  <el-icon class="delivery-icon"><Clock /></el-icon>
                  <div class="delivery-text">
                    <h4>配送时间</h4>
                    <p>预计30-45分钟送达</p>
                  </div>
                </div>
                <div class="delivery-item">
                  <el-icon class="delivery-icon"><MapLocation /></el-icon>
                  <div class="delivery-text">
                    <h4>配送范围</h4>
                    <p>限市区5公里内</p>
                  </div>
                </div>
                <div class="delivery-item">
                  <el-icon class="delivery-icon"><Service /></el-icon>
                  <div class="delivery-text">
                    <h4>售后服务</h4>
                    <p>支持7天无理由退换</p>
                  </div>
                </div>
              </div>
            </el-card>
          </div>
        </el-col>
      </el-row>
    </div>

    <!-- 移除商品确认对话框 -->
    <el-dialog
      v-model="removeDialogVisible"
      title="确认移除"
      width="400px"
    >
      <p>确定要从购物车中移除 <strong>{{ selectedItem?.name }}</strong> 吗？</p>
      <template #footer>
        <el-button @click="removeDialogVisible = false">取消</el-button>
        <el-button
          type="danger"
          @click="confirmRemoveItem"
          :loading="removingItem"
        >
          确定移除
        </el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ShoppingCart,
  Delete,
  CreditCard,
  Clock,
  MapLocation,
  Service
} from '@element-plus/icons-vue'
import { useCartStore } from '@/store/cart'
import { useAuthStore } from '@/store/auth'
import menuAPI from '@/api/menu'
import CoffeeCard from '@/components/CoffeeCard.vue'

// 路由和状态管理
const router = useRouter()
const cartStore = useCartStore()
const authStore = useAuthStore()

// 响应式数据
const couponCode = ref('')
const applyingCoupon = ref(false)
const removeDialogVisible = ref(false)
const selectedItem = ref(null)
const removingItem = ref(false)
const recommendations = ref([])

// 配送费配置
const DELIVERY_FEE_THRESHOLD = 30 // 免配送费门槛
const DELIVERY_FEE = 5 // 配送费

// 计算属性
const cartItems = computed(() => cartStore.items)

const cartItemsCount = computed(() => cartStore.totalItems)

const subtotal = computed(() => cartStore.totalPrice)

const discount = computed(() => {
  // 这里可以根据优惠券计算折扣
  return 0 // 暂时没有折扣
})

const deliveryFee = computed(() => {
  return subtotal.value >= DELIVERY_FEE_THRESHOLD ? 0 : DELIVERY_FEE
})

const totalPrice = computed(() => {
  return Math.max(0, subtotal.value - discount.value + deliveryFee.value)
})

// 方法
const handleImageError = (event) => {
  event.target.src = '/default-coffee.jpg'
}

const getItemAnimationDelay = (itemId) => {
  const index = cartItems.value.findIndex(item => item.id === itemId)
  return index * 50
}

const handleQuantityChange = async (item, quantity) => {
  if (quantity < 1) return
  if (quantity > 99) return

  try {
    await cartStore.updateQuantity(item.id, quantity)
    ElMessage.success('数量已更新')
  } catch (error) {
    console.error('更新数量失败:', error)
    ElMessage.error('更新数量失败，请稍后重试')
  }
}

const handleRemoveItem = (item) => {
  selectedItem.value = item
  removeDialogVisible.value = true
}

const confirmRemoveItem = async () => {
  if (!selectedItem.value) return

  removingItem.value = true

  try {
    await cartStore.removeItem(selectedItem.value.id)
    ElMessage.success(`${selectedItem.value.name} 已从购物车移除`)
    removeDialogVisible.value = false
  } catch (error) {
    console.error('移除商品失败:', error)
    ElMessage.error('移除商品失败，请稍后重试')
  } finally {
    removingItem.value = false
  }
}

const clearCart = async () => {
  try {
    await ElMessageBox.confirm(
      '确定要清空购物车吗？此操作不可恢复。',
      '确认清空',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await cartStore.clearCart()
    ElMessage.success('购物车已清空')
  } catch (error) {
    if (error !== 'cancel') {
      console.error('清空购物车失败:', error)
      ElMessage.error('清空购物车失败，请稍后重试')
    }
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

const applyCoupon = async () => {
  if (!couponCode.value.trim()) return

  applyingCoupon.value = true

  try {
    // 这里应该调用优惠券API
    // await cartStore.applyCoupon(couponCode.value.trim())
    ElMessage.success('优惠券应用成功')
  } catch (error) {
    console.error('应用优惠券失败:', error)
    ElMessage.error('优惠券无效或已过期')
  } finally {
    applyingCoupon.value = false
  }
}

const handleCheckout = () => {
  if (!authStore.isAuthenticated) {
    ElMessageBox.confirm(
      '请先登录后再进行结算',
      '提示',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'info'
      }
    ).then(() => {
      authStore.setRedirectPath('/cart')
      router.push('/login')
    }).catch(() => {
      // 用户取消
    })
    return
  }

  // 跳转到结算页面
  router.push('/checkout')
}

const goToMenu = () => {
  router.push('/menu')
}

const loadRecommendations = async () => {
  try {
    const response = await menuAPI.getPopularItems({ limit: 4 })
    recommendations.value = response.data || []
  } catch (error) {
    console.error('加载推荐商品失败:', error)
    recommendations.value = []
  }
}

// 生命周期
onMounted(() => {
  // 加载推荐商品
  loadRecommendations()
})
</script>

<style lang="scss" scoped>
.cart-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 100px 20px 40px;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;

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

.cart-container {
  max-width: 1200px;
  margin: 0 auto;
}

.cart-card,
.recommendations-card {
  margin-bottom: 24px;
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

  :deep(.el-card__header) {
    border-bottom: 1px solid #f0f0f0;
    background: #f8f9fa;
  }

  .card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;

    h3 {
      margin: 0;
      color: #2c3e50;
      font-size: 1.2rem;
    }

    .clear-btn {
      color: #e74c3c;
      font-size: 0.9rem;

      &:hover {
        background: rgba(231, 76, 60, 0.1);
      }
    }
  }
}

.empty-cart {
  padding: 60px 20px;
  text-align: center;
}

.cart-items {
  .cart-item {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 20px 0;
    border-bottom: 1px solid #f0f0f0;

    &:last-child {
      border-bottom: none;
    }

    .item-image {
      width: 80px;
      height: 80px;
      border-radius: 8px;
      overflow: hidden;
      flex-shrink: 0;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    .item-info {
      flex: 1;
      min-width: 0;

      .item-name {
        margin: 0 0 8px 0;
        font-size: 1.1rem;
        color: #2c3e50;
        font-weight: 500;
      }

      .item-description {
        margin: 0 0 8px 0;
        font-size: 0.9rem;
        color: #7f8c8d;
        line-height: 1.4;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
        overflow: hidden;
        text-overflow: ellipsis;
      }

      .item-tags {
        display: flex;
        gap: 6px;
        flex-wrap: wrap;
      }
    }

    .item-price {
      display: flex;
      flex-direction: column;
      align-items: flex-end;
      gap: 4px;
      min-width: 100px;
      flex-shrink: 0;

      .price-info {
        display: flex;
        align-items: center;
        gap: 8px;

        .current-price {
          font-size: 1.1rem;
          font-weight: bold;
          color: #e74c3c;
        }

        .original-price {
          font-size: 0.9rem;
          color: #95a5a6;
          text-decoration: line-through;
        }
      }

      .item-subtotal {
        font-size: 0.9rem;
        color: #7f8c8d;
        font-weight: 500;
      }
    }

    .item-quantity {
      flex-shrink: 0;

      :deep(.el-input-number) {
        width: 120px;
      }
    }

    .item-actions {
      flex-shrink: 0;

      .remove-btn {
        color: #e74c3c;
        padding: 8px;
        font-size: 0.9rem;

        &:hover {
          background: rgba(231, 76, 60, 0.1);
        }
      }
    }
  }
}

.recommendations-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 16px;
}

.order-summary {
  position: sticky;
  top: 100px;
}

.summary-card,
.delivery-card {
  margin-bottom: 24px;
  border-radius: 12px;
  border: none;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);

  :deep(.el-card__header) {
    border-bottom: 1px solid #f0f0f0;
    background: #f8f9fa;

    h3 {
      margin: 0;
      color: #2c3e50;
      font-size: 1.2rem;
    }
  }
}

.summary-content {
  .coupon-section {
    margin-bottom: 24px;
  }

  .price-details {
    margin-bottom: 24px;

    .price-row {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      font-size: 1rem;

      &.discount {
        color: #27ae60;
      }

      &.total {
        font-weight: bold;
        font-size: 1.1rem;
        color: #2c3e50;
      }

      .total-price {
        font-size: 1.3rem;
        font-weight: bold;
        color: #e74c3c;
      }
    }

    .price-divider {
      height: 1px;
      background: #e0e0e0;
      margin: 16px 0;
    }
  }

  .delivery-info {
    margin-bottom: 24px;
  }

  .checkout-section {
    .checkout-btn {
      width: 100%;
      height: 48px;
      font-size: 1.1rem;
      border-radius: 24px;
      background: linear-gradient(135deg, #8b4513, #a0522d);
      border: none;

      &:hover {
        background: linear-gradient(135deg, #a0522d, #8b4513);
        transform: translateY(-2px);
      }

      &:disabled {
        background: #bdc3c7;
        transform: none;
      }
    }
  }
}

.delivery-content {
  .delivery-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 0;

    &:not(:last-child) {
      border-bottom: 1px solid #f0f0f0;
    }

    .delivery-icon {
      font-size: 1.5rem;
      color: #8b4513;
      flex-shrink: 0;
    }

    .delivery-text {
      h4 {
        margin: 0 0 4px 0;
        font-size: 1rem;
        color: #2c3e50;
      }

      p {
        margin: 0;
        font-size: 0.9rem;
        color: #7f8c8d;
      }
    }
  }
}

// 响应式设计
@media (max-width: 1024px) {
  .order-summary {
    position: static;
    margin-top: 24px;
  }
}

@media (max-width: 768px) {
  .cart-page {
    padding: 80px 16px 32px;
  }

  .page-title {
    font-size: 2rem !important;

    .title-icon {
      font-size: 1.8rem !important;
    }
  }

  .cart-item {
    flex-direction: column;
    align-items: stretch;
    gap: 12px;

    .item-image {
      align-self: center;
      width: 120px;
      height: 120px;
    }

    .item-price {
      align-items: flex-start;
    }

    .item-quantity {
      align-self: center;
    }

    .item-actions {
      align-self: center;
    }
  }

  .recommendations-grid {
    grid-template-columns: repeat(auto-fill, minmax(160px, 1fr));
    gap: 12px;
  }
}

@media (max-width: 480px) {
  .cart-page {
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

  .cart-item {
    .item-image {
      width: 100px;
      height: 100px;
    }
  }

  .recommendations-grid {
    grid-template-columns: 1fr;
  }
}
</style>