<template>
  <el-card class="coffee-card" :class="{ 'out-of-stock': !item.is_available }" shadow="hover">
    <!-- 商品图片 -->
    <div class="card-image">
      <img
        :src="item.image_url || '/default-coffee.jpg'"
        :alt="item.name"
        @error="handleImageError"
      />

      <!-- 折扣标签 -->
      <div v-if="hasDiscount" class="discount-badge">
        -{{ discountPercentage }}%
      </div>

      <!-- 热门标签 -->
      <div v-if="item.is_popular" class="popular-badge">
        <el-icon><Star /></el-icon>
        热门
      </div>

      <!-- 售罄遮罩 -->
      <div v-if="!item.is_available" class="out-of-stock-overlay">
        <span>暂时售罄</span>
      </div>
    </div>

    <!-- 商品信息 -->
    <div class="card-content">
      <!-- 商品名称和分类 -->
      <div class="item-header">
        <h3 class="item-name" :title="item.name">{{ item.name }}</h3>
        <el-tag size="small" type="info" class="category-tag">
          {{ categoryLabel }}
        </el-tag>
      </div>

      <!-- 商品描述 -->
      <p class="item-description" :title="item.description">
        {{ item.description }}
      </p>

      <!-- 价格信息 -->
      <div class="price-section">
        <div class="price-info">
          <span class="current-price">¥{{ item.price }}</span>
          <span v-if="item.original_price && item.original_price > item.price" class="original-price">
            ¥{{ item.original_price }}
          </span>
        </div>

        <!-- 销量信息 -->
        <div v-if="item.order_count > 0" class="sales-info">
          已售 {{ item.order_count }} 杯
        </div>
      </div>

      <!-- 操作按钮 -->
      <div class="action-section">
        <!-- 数量选择器 -->
        <div class="quantity-selector" v-if="item.is_available">
          <el-input-number
            v-model="quantity"
            :min="1"
            :max="99"
            size="small"
            controls-position="right"
            @change="handleQuantityChange"
          />
        </div>

        <!-- 操作按钮组 -->
        <div class="action-buttons">
          <!-- 查看详情按钮 -->
          <el-button
            type="info"
            size="small"
            :icon="View"
            circle
            @click="handleViewDetail"
            class="detail-btn"
          />

          <!-- 加入购物车按钮 -->
          <el-button
            v-if="item.is_available"
            type="primary"
            size="small"
            :icon="ShoppingCart"
            :loading="adding"
            @click="handleAddToCart"
            class="add-to-cart-btn"
          >
            加入购物车
          </el-button>

          <!-- 到货通知按钮（售罄时显示） -->
          <el-button
            v-else
            type="warning"
            size="small"
            :icon="Bell"
            @click="handleNotifyWhenAvailable"
            class="notify-btn"
          >
            到货通知
          </el-button>
        </div>
      </div>

      <!-- 标签区域 -->
      <div class="tags-section" v-if="item.tags && item.tags.length > 0">
        <el-tag
          v-for="tag in item.tags"
          :key="tag"
          size="small"
          effect="light"
          class="item-tag"
        >
          {{ tag }}
        </el-tag>
      </div>
    </div>

    <!-- 快速操作浮动按钮 -->
    <div class="quick-actions" v-if="item.is_available && showQuickActions">
      <el-button
        type="primary"
        size="small"
        :icon="Plus"
        circle
        @click="handleQuickAdd"
        class="quick-add-btn"
      />
    </div>
  </el-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ElMessage } from 'element-plus'
import {
  ShoppingCart,
  View,
  Bell,
  Plus,
  Star
} from '@element-plus/icons-vue'

// Props
const props = defineProps({
  item: {
    type: Object,
    required: true
  },
  categoryLabel: {
    type: String,
    default: '咖啡'
  },
  showQuickActions: {
    type: Boolean,
    default: true
  }
})

// Emits
const emit = defineEmits(['add-to-cart', 'view-detail', 'notify-when-available'])

// 响应式数据
const quantity = ref(1)
const adding = ref(false)

// 计算属性
const hasDiscount = computed(() => {
  return props.item.original_price && props.item.original_price > props.item.price
})

const discountPercentage = computed(() => {
  if (!hasDiscount.value) return 0
  return Math.round(
    ((props.item.original_price - props.item.price) / props.item.original_price) * 100
  )
})

// 方法
const handleImageError = (event) => {
  // 图片加载失败时使用默认图片
  event.target.src = '/default-coffee.jpg'
}

const handleQuantityChange = (value) => {
  // 确保数量在合理范围内
  if (value < 1) quantity.value = 1
  if (value > 99) quantity.value = 99
}

const handleAddToCart = async () => {
  if (adding.value) return

  adding.value = true

  try {
    await emit('add-to-cart', props.item, quantity.value)
    // 重置数量为1
    quantity.value = 1
  } catch (error) {
    console.error('添加到购物车失败:', error)
  } finally {
    adding.value = false
  }
}

const handleQuickAdd = async () => {
  // 快速添加（数量为1）
  await emit('add-to-cart', props.item, 1)
}

const handleViewDetail = () => {
  emit('view-detail', props.item)
}

const handleNotifyWhenAvailable = () => {
  emit('notify-when-available', props.item)
}
</script>

<style lang="scss" scoped>
.coffee-card {
  height: 100%;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;

  &:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
    border-color: #8b4513;

    .quick-actions {
      opacity: 1;
      transform: scale(1);
    }
  }

  &.out-of-stock {
    opacity: 0.8;
    background: #f8f9fa;

    .card-image {
      position: relative;

      &::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(255, 255, 255, 0.7);
        z-index: 1;
      }
    }
  }

  :deep(.el-card__body) {
    padding: 0;
    height: 100%;
    display: flex;
    flex-direction: column;
  }
}

.card-image {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;

  img {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.3s ease;

    .coffee-card:hover & {
      transform: scale(1.05);
    }
  }

  .discount-badge {
    position: absolute;
    top: 10px;
    left: 10px;
    background: #e74c3c;
    color: white;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: bold;
    z-index: 2;
  }

  .popular-badge {
    position: absolute;
    top: 10px;
    right: 10px;
    background: linear-gradient(135deg, #f39c12, #e67e22);
    color: white;
    padding: 4px 8px;
    border-radius: 6px;
    font-size: 0.8rem;
    font-weight: bold;
    display: flex;
    align-items: center;
    gap: 4px;
    z-index: 2;

    .el-icon {
      font-size: 0.8rem;
    }
  }

  .out-of-stock-overlay {
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.6);
    display: flex;
    align-items: center;
    justify-content: center;
    z-index: 3;

    span {
      color: white;
      font-size: 1.2rem;
      font-weight: bold;
      background: rgba(231, 76, 60, 0.9);
      padding: 8px 16px;
      border-radius: 8px;
    }
  }
}

.card-content {
  padding: 16px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;

  .item-name {
    font-size: 1.1rem;
    font-weight: bold;
    color: #2c3e50;
    margin: 0;
    flex: 1;
    margin-right: 8px;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    text-overflow: ellipsis;
  }

  .category-tag {
    flex-shrink: 0;
  }
}

.item-description {
  color: #7f8c8d;
  font-size: 0.9rem;
  line-height: 1.4;
  margin: 0 0 12px 0;
  flex: 1;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
  text-overflow: ellipsis;
}

.price-section {
  margin-bottom: 16px;

  .price-info {
    display: flex;
    align-items: center;
    gap: 8px;
    margin-bottom: 4px;

    .current-price {
      font-size: 1.3rem;
      font-weight: bold;
      color: #e74c3c;
    }

    .original-price {
      font-size: 1rem;
      color: #95a5a6;
      text-decoration: line-through;
    }
  }

  .sales-info {
    font-size: 0.8rem;
    color: #95a5a6;
  }
}

.action-section {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;

  .quantity-selector {
    flex-shrink: 0;

    :deep(.el-input-number) {
      width: 100px;
    }
  }

  .action-buttons {
    flex: 1;
    display: flex;
    gap: 8px;

    .detail-btn,
    .add-to-cart-btn,
    .notify-btn {
      border-radius: 20px;
      transition: all 0.3s ease;

      &:hover {
        transform: translateY(-2px);
      }
    }

    .add-to-cart-btn {
      flex: 1;
      background: linear-gradient(135deg, #8b4513, #a0522d);
      border: none;

      &:hover {
        background: linear-gradient(135deg, #a0522d, #8b4513);
      }
    }

    .notify-btn {
      flex: 1;
      background: linear-gradient(135deg, #f39c12, #e67e22);
      border: none;

      &:hover {
        background: linear-gradient(135deg, #e67e22, #f39c12);
      }
    }
  }
}

.tags-section {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: auto;

  .item-tag {
    font-size: 0.7rem;
    height: 20px;
    line-height: 20px;
  }
}

.quick-actions {
  position: absolute;
  bottom: 16px;
  right: 16px;
  opacity: 0;
  transform: scale(0.8);
  transition: all 0.3s ease;
  z-index: 4;

  .quick-add-btn {
    width: 40px;
    height: 40px;
    background: linear-gradient(135deg, #27ae60, #2ecc71);
    border: none;
    box-shadow: 0 4px 12px rgba(39, 174, 96, 0.4);

    &:hover {
      background: linear-gradient(135deg, #2ecc71, #27ae60);
      transform: scale(1.1);
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .coffee-card {
    .card-image {
      height: 160px;
    }

    .card-content {
      padding: 12px;
    }

    .item-header {
      flex-direction: column;
      align-items: flex-start;
      gap: 8px;

      .item-name {
        margin-right: 0;
        -webkit-line-clamp: 1;
      }
    }

    .item-description {
      -webkit-line-clamp: 2;
      font-size: 0.85rem;
    }

    .action-section {
      flex-direction: column;
      align-items: stretch;
      gap: 8px;

      .quantity-selector {
        align-self: flex-start;
      }

      .action-buttons {
        .detail-btn,
        .add-to-cart-btn,
        .notify-btn {
          font-size: 0.85rem;
          padding: 6px 12px;
        }
      }
    }
  }
}
</style>