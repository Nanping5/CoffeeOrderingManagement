<template>
  <!-- 购物车浮动按钮 -->
  <transition name="float-button">
    <div
      v-if="showButton && cartItemsCount > 0"
      class="cart-float-button"
      :class="{ 'button-pulse': isPulse }"
      @click="handleClick"
    >
      <!-- 徽章显示商品数量 -->
      <el-badge
        :value="cartItemsCount"
        :max="99"
        class="cart-badge"
      >
        <div class="button-content">
          <el-icon class="cart-icon"><ShoppingCart /></el-icon>
        </div>
      </el-badge>

      <!-- 总价格显示 -->
      <div class="price-display" v-if="showPrice">
        ¥{{ totalPrice.toFixed(2) }}
      </div>
    </div>
  </transition>

  <!-- 快速预览购物车弹窗 -->
  <transition name="preview">
    <div
      v-if="showPreview"
      class="cart-preview"
      :class="{ 'preview-expanded': isExpanded }"
    >
      <!-- 预览头部 -->
      <div class="preview-header">
        <h4>购物车 ({{ cartItemsCount }})</h4>
        <el-button
          type="text"
          :icon="Close"
          @click="closePreview"
          class="close-btn"
        />
      </div>

      <!-- 购物车商品列表 -->
      <div class="preview-content">
        <div
          v-for="item in previewItems"
          :key="item.id"
          class="preview-item"
        >
          <div class="item-image">
            <img
              :src="item.image_url || '/default-coffee.jpg'"
              :alt="item.name"
              @error="handleImageError"
            />
          </div>
          <div class="item-info">
            <h5 class="item-name">{{ item.name }}</h5>
            <p class="item-price">¥{{ item.price }} x {{ item.quantity }}</p>
          </div>
          <div class="item-actions">
            <el-input-number
              :model-value="item.quantity"
              :min="1"
              :max="99"
              size="small"
              @change="handleQuantityChange(item, $event)"
            />
            <el-button
              type="text"
              :icon="Delete"
              size="small"
              @click="handleRemoveItem(item)"
              class="remove-btn"
            />
          </div>
        </div>

        <!-- 空状态 -->
        <div v-if="previewItems.length === 0" class="empty-preview">
          <el-empty description="购物车是空的" :image-size="80" />
        </div>
      </div>

      <!-- 预览底部 -->
      <div class="preview-footer">
        <div class="total-info">
          <span>总计：</span>
          <span class="total-price">¥{{ totalPrice.toFixed(2) }}</span>
        </div>
        <div class="footer-actions">
          <el-button @click="viewCart">查看购物车</el-button>
          <el-button
            type="primary"
            :disabled="cartItemsCount === 0"
            @click="checkout"
          >
            去结算
          </el-button>
        </div>
      </div>
    </div>
  </transition>

  <!-- 遮罩层 -->
  <transition name="mask">
    <div
      v-if="showPreview"
      class="preview-mask"
      @click="closePreview"
    ></div>
  </transition>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  ShoppingCart,
  Close,
  Delete
} from '@element-plus/icons-vue'
import { useCartStore } from '@/store/cart'
import { useAuthStore } from '@/store/auth'

// Props
const props = defineProps({
  showPrice: {
    type: Boolean,
    default: true
  },
  showOnRoutes: {
    type: Array,
    default: () => ['Menu']
  }
})

// 路由和状态管理
const router = useRouter()
const route = useRoute()
const cartStore = useCartStore()
const authStore = useAuthStore()

// 响应式数据
const showPreview = ref(false)
const isExpanded = ref(false)
const isPulse = ref(false)
const scrollY = ref(0)

// 计算属性
const showButton = computed(() => {
  // 只在指定路由显示浮动按钮
  return props.showOnRoutes.includes(route.name)
})

const cartItemsCount = computed(() => {
  return cartStore.totalItems
})

const totalPrice = computed(() => {
  return cartStore.totalPrice
})

const previewItems = computed(() => {
  // 最多显示3个商品
  return cartStore.items.slice(0, 3)
})

// 方法
const handleClick = () => {
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
      authStore.setRedirectPath(route.fullPath)
      router.push('/login')
    }).catch(() => {
      // 用户取消
    })
    return
  }

  // 如果预览窗口已打开，则跳转到购物车页面
  if (showPreview.value) {
    viewCart()
  } else {
    showPreview.value = true
    isExpanded.value = true
  }
}

const closePreview = () => {
  isExpanded.value = false
  setTimeout(() => {
    showPreview.value = false
  }, 300)
}

const handleQuantityChange = async (item, quantity) => {
  try {
    await cartStore.updateQuantity(item.id, quantity)
    ElMessage.success('数量已更新')
  } catch (error) {
    console.error('更新数量失败:', error)
    ElMessage.error('更新数量失败，请稍后重试')
  }
}

const handleRemoveItem = async (item) => {
  try {
    await ElMessageBox.confirm(
      `确定要移除 ${item.name} 吗？`,
      '提示',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }
    )

    await cartStore.removeItem(item.id)
    ElMessage.success(`${item.name} 已从购物车移除`)

    // 如果购物车为空，关闭预览
    if (cartStore.items.length === 0) {
      closePreview()
    }
  } catch (error) {
    if (error !== 'cancel') {
      console.error('移除商品失败:', error)
      ElMessage.error('移除商品失败，请稍后重试')
    }
  }
}

const viewCart = () => {
  closePreview()
  router.push('/cart')
}

const checkout = () => {
  closePreview()
  router.push('/checkout')
}

const handleImageError = (event) => {
  event.target.src = '/default-coffee.jpg'
}

const handleScroll = () => {
  const currentScrollY = window.scrollY
  scrollY.value = currentScrollY

  // 滚动时显示脉冲效果
  if (currentScrollY > 100 && !isPulse.value) {
    isPulse.value = true
    setTimeout(() => {
      isPulse.value = false
    }, 1000)
  }
}

// 监听购物车变化，显示脉冲效果
watch(cartItemsCount, (newCount, oldCount) => {
  if (newCount > oldCount) {
    // 添加商品时显示脉冲效果
    isPulse.value = true
    setTimeout(() => {
      isPulse.value = false
    }, 1000)
  }
})

// 生命周期
onMounted(() => {
  window.addEventListener('scroll', handleScroll)
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
})
</script>

<style lang="scss" scoped>
.cart-float-button {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 999;
  cursor: pointer;
  transition: all 0.3s ease;
  background: linear-gradient(135deg, #8b4513, #a0522d);
  border-radius: 50%;
  width: 60px;
  height: 60px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 20px rgba(139, 69, 19, 0.4);
  border: 3px solid white;

  &:hover {
    transform: translateY(-5px) scale(1.1);
    box-shadow: 0 8px 30px rgba(139, 69, 19, 0.6);
  }

  &.button-pulse {
    animation: pulse 1s ease-in-out;
  }

  .cart-badge {
    :deep(.el-badge__content) {
      background: #e74c3c;
      border: 2px solid white;
      font-size: 0.7rem;
      min-width: 18px;
      height: 18px;
      line-height: 18px;
    }
  }

  .button-content {
    color: white;
    font-size: 1.5rem;

    .cart-icon {
      font-size: 1.5rem;
    }
  }

  .price-display {
    position: absolute;
    top: -8px;
    left: -8px;
    background: #e74c3c;
    color: white;
    padding: 4px 8px;
    border-radius: 12px;
    font-size: 0.7rem;
    font-weight: bold;
    white-space: nowrap;
    box-shadow: 0 2px 8px rgba(231, 76, 60, 0.4);
  }
}

.cart-preview {
  position: fixed;
  bottom: 90px;
  right: 24px;
  width: 360px;
  max-height: 500px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.15);
  z-index: 998;
  overflow: hidden;
  transform: scale(0.9) translateY(20px);
  opacity: 0;
  transition: all 0.3s ease;

  &.preview-expanded {
    transform: scale(1) translateY(0);
    opacity: 1;
  }

  .preview-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 16px 20px;
    border-bottom: 1px solid #f0f0f0;
    background: linear-gradient(135deg, #f8f9fa, #e9ecef);

    h4 {
      margin: 0;
      color: #2c3e50;
      font-size: 1.1rem;
    }

    .close-btn {
      color: #7f8c8d;
      padding: 4px;

      &:hover {
        color: #e74c3c;
      }
    }
  }

  .preview-content {
    max-height: 300px;
    overflow-y: auto;
    padding: 16px 20px;

    .preview-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 0;
      border-bottom: 1px solid #f8f9fa;

      &:last-child {
        border-bottom: none;
      }

      .item-image {
        width: 50px;
        height: 50px;
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
          margin: 0 0 4px 0;
          font-size: 0.9rem;
          color: #2c3e50;
          font-weight: 500;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }

        .item-price {
          margin: 0;
          font-size: 0.8rem;
          color: #e74c3c;
          font-weight: 500;
        }
      }

      .item-actions {
        display: flex;
        align-items: center;
        gap: 8px;
        flex-shrink: 0;

        :deep(.el-input-number) {
          width: 80px;
        }

        .remove-btn {
          color: #e74c3c;
          padding: 4px;

          &:hover {
            background: rgba(231, 76, 60, 0.1);
          }
        }
      }
    }

    .empty-preview {
      padding: 40px 20px;
      text-align: center;
    }
  }

  .preview-footer {
    padding: 16px 20px;
    border-top: 1px solid #f0f0f0;
    background: #f8f9fa;

    .total-info {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 12px;
      font-size: 1rem;

      .total-price {
        font-size: 1.2rem;
        font-weight: bold;
        color: #e74c3c;
      }
    }

    .footer-actions {
      display: flex;
      gap: 12px;

      .el-button {
        flex: 1;
        border-radius: 20px;
      }
    }
  }
}

.preview-mask {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.3);
  z-index: 997;
  backdrop-filter: blur(2px);
}

// 动画
@keyframes pulse {
  0% {
    transform: scale(1);
    box-shadow: 0 4px 20px rgba(139, 69, 19, 0.4);
  }

  50% {
    transform: scale(1.1);
    box-shadow: 0 8px 30px rgba(139, 69, 19, 0.8);
  }

  100% {
    transform: scale(1);
    box-shadow: 0 4px 20px rgba(139, 69, 19, 0.4);
  }
}

.float-button-enter-active,
.float-button-leave-active {
  transition: all 0.3s ease;
}

.float-button-enter-from {
  transform: scale(0);
  opacity: 0;
}

.float-button-leave-to {
  transform: scale(0);
  opacity: 0;
}

.preview-enter-active,
.preview-leave-active {
  transition: all 0.3s ease;
}

.preview-enter-from,
.preview-leave-to {
  transform: scale(0.9) translateY(20px);
  opacity: 0;
}

.mask-enter-active,
.mask-leave-active {
  transition: opacity 0.3s ease;
}

.mask-enter-from,
.mask-leave-to {
  opacity: 0;
}

// 响应式设计
@media (max-width: 768px) {
  .cart-float-button {
    bottom: 20px;
    right: 20px;
    width: 56px;
    height: 56px;

    .button-content {
      font-size: 1.3rem;

      .cart-icon {
        font-size: 1.3rem;
      }
    }

    .price-display {
      font-size: 0.65rem;
    }
  }

  .cart-preview {
    width: calc(100vw - 40px);
    right: 20px;
    bottom: 80px;
    max-height: 60vh;
  }
}

@media (max-width: 480px) {
  .cart-float-button {
    bottom: 16px;
    right: 16px;
    width: 52px;
    height: 52px;

    .button-content {
      font-size: 1.2rem;

      .cart-icon {
        font-size: 1.2rem;
      }
    }

    .price-display {
      display: none; // 在小屏幕上隐藏价格显示
    }
  }

  .cart-preview {
    width: calc(100vw - 32px);
    right: 16px;
    bottom: 70px;

    .preview-content {
      .preview-item {
        .item-info {
          .item-name {
            font-size: 0.85rem;
          }

          .item-price {
            font-size: 0.75rem;
          }
        }
      }
    }
  }
}
</style>