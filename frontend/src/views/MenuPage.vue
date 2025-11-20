<template>
  <div class="menu-page">
    <!-- 页面头部 -->
    <div class="page-header animate__animated animate__fadeInDown">
      <div class="header-content">
        <h1 class="page-title">
          <el-icon class="title-icon"><Coffee /></el-icon>
          咖啡菜单
        </h1>
        <p class="page-subtitle">精选优质咖啡，为您带来美好的味蕾体验</p>
      </div>
    </div>

    <!-- 筛选和搜索区域 -->
    <div class="filter-section animate__animated animate__fadeInUp">
      <el-card class="filter-card" shadow="hover">
        <div class="filter-content">
          <!-- 搜索框 -->
          <div class="search-box">
            <el-input
              v-model="searchQuery"
              placeholder="搜索您喜欢的咖啡..."
              prefix-icon="Search"
              clearable
              @input="handleSearch"
              class="search-input"
            />
          </div>

          <!-- 分类筛选 -->
          <div class="category-filter">
            <el-radio-group v-model="selectedCategory" @change="handleCategoryChange">
              <el-radio-button
                v-for="category in categories"
                :key="category.value"
                :label="category.value"
              >
                {{ category.label }}
              </el-radio-button>
            </el-radio-group>
          </div>

          <!-- 排序选项 -->
          <div class="sort-options">
            <el-select v-model="sortBy" placeholder="排序方式" @change="handleSort">
              <el-option label="默认排序" value="default" />
              <el-option label="价格从低到高" value="price_asc" />
              <el-option label="价格从高到低" value="price_desc" />
              <el-option label="最受欢迎" value="popular" />
              <el-option label="最新上架" value="newest" />
            </el-select>
          </div>
        </div>
      </el-card>
    </div>

    <!-- 菜单内容区域 -->
    <div class="menu-content">
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-container">
        <el-skeleton :rows="6" animated />
      </div>

      <!-- 空状态 -->
      <div v-else-if="menuItems.length === 0" class="empty-state">
        <el-empty description="暂无商品">
          <template #image>
            <el-icon size="60"><Coffee /></el-icon>
          </template>
          <el-button type="primary" @click="resetFilters">重置筛选</el-button>
        </el-empty>
      </div>

      <!-- 菜单网格 -->
      <div v-else class="menu-grid animate__animated animate__fadeIn">
        <div
          v-for="item in menuItems"
          :key="item.id"
          class="menu-item-wrapper animate__animated animate__fadeInUp"
          :style="{ 'animation-delay': `${getItemAnimationDelay(item.id)}ms` }"
        >
          <CoffeeCard
            :item="item"
            @add-to-cart="handleAddToCart"
            @view-detail="handleViewDetail"
          />
        </div>
      </div>

      <!-- 加载更多 -->
      <div v-if="hasMore && !loading" class="load-more">
        <el-button
          type="primary"
          :loading="loadingMore"
          @click="loadMore"
          class="load-more-btn"
        >
          {{ loadingMore ? '加载中...' : '加载更多' }}
        </el-button>
      </div>
    </div>

    <!-- 商品详情弹窗 -->
    <el-dialog
      v-model="detailDialogVisible"
      :title="selectedItem?.name"
      width="600px"
      class="detail-dialog"
      destroy-on-close
    >
      <div v-if="selectedItem" class="item-detail">
        <div class="detail-image">
          <img :src="selectedItem.image_url || '/default-coffee.jpg'" :alt="selectedItem.name" />
        </div>
        <div class="detail-info">
          <h3>{{ selectedItem.name }}</h3>
          <p class="description">{{ selectedItem.description }}</p>
          <div class="price-info">
            <span class="price">¥{{ selectedItem.price }}</span>
            <span v-if="selectedItem.original_price" class="original-price">
              ¥{{ selectedItem.original_price }}
            </span>
          </div>
          <div class="category-tag">
            <el-tag type="info">{{ getCategoryLabel(selectedItem.category) }}</el-tag>
          </div>
        </div>
      </div>

      <template #footer>
        <span class="dialog-footer">
          <el-button @click="detailDialogVisible = false">取消</el-button>
          <el-button
            type="primary"
            @click="handleAddToCartFromDetail"
            :loading="addingToCart"
          >
            <el-icon><ShoppingCart /></el-icon>
            加入购物车
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Coffee, ShoppingCart, Search } from '@element-plus/icons-vue'
import { useCartStore } from '@/store/cart'
import { useAuthStore } from '@/store/auth'
import menuAPI from '@/api/menu'
import CoffeeCard from '@/components/CoffeeCard.vue'

// 状态管理
const cartStore = useCartStore()
const authStore = useAuthStore()

// 响应式数据
const loading = ref(false)
const loadingMore = ref(false)
const menuItems = ref([])
const categories = ref([])
const searchQuery = ref('')
const selectedCategory = ref('all')
const sortBy = ref('default')
const currentPage = ref(1)
const pageSize = ref(12)
const hasMore = ref(true)
const detailDialogVisible = ref(false)
const selectedItem = ref(null)
const addingToCart = ref(false)

// 分页数据
const pagination = reactive({
  current: 1,
  size: 12,
  total: 0
})

// 计算属性
const filteredItems = computed(() => {
  let items = menuItems.value

  // 搜索过滤
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    items = items.filter(item =>
      item.name.toLowerCase().includes(query) ||
      item.description.toLowerCase().includes(query)
    )
  }

  // 分类过滤
  if (selectedCategory.value !== 'all') {
    items = items.filter(item => item.category === selectedCategory.value)
  }

  // 排序
  switch (sortBy.value) {
    case 'price_asc':
      items.sort((a, b) => a.price - b.price)
      break
    case 'price_desc':
      items.sort((a, b) => b.price - a.price)
      break
    case 'popular':
      items.sort((a, b) => (b.order_count || 0) - (a.order_count || 0))
      break
    case 'newest':
      items.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
      break
  }

  return items
})

// 方法
const getMenuList = async (reset = false) => {
  if (reset) {
    currentPage.value = 1
    menuItems.value = []
    hasMore.value = true
  }

  loading.value = true

  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      category: selectedCategory.value === 'all' ? undefined : selectedCategory.value,
      keyword: searchQuery.value || undefined
    }

    const response = await menuAPI.getMenuList(params)

    if (reset) {
      menuItems.value = response.data.items || []
    } else {
      menuItems.value.push(...(response.data.items || []))
    }

    pagination.total = response.data.total || 0
    hasMore.value = menuItems.value.length < pagination.total

  } catch (error) {
    console.error('获取菜单列表失败:', error)
    ElMessage.error('获取菜单列表失败，请稍后重试')
  } finally {
    loading.value = false
  }
}

const getCategories = async () => {
  try {
    const response = await menuAPI.getCategories()
    categories.value = [
      { value: 'all', label: '全部' },
      ...(response.data || [])
    ]
  } catch (error) {
    console.error('获取分类列表失败:', error)
    // 设置默认分类
    categories.value = [
      { value: 'all', label: '全部' },
      { value: 'coffee', label: '咖啡' },
      { value: 'tea', label: '茶饮' },
      { value: 'dessert', label: '甜点' },
      { value: 'other', label: '其他' }
    ]
  }
}

const handleSearch = (query) => {
  // 防抖处理
  clearTimeout(handleSearch.debounceTimer)
  handleSearch.debounceTimer = setTimeout(() => {
    getMenuList(true)
  }, 500)
}

const handleCategoryChange = () => {
  getMenuList(true)
}

const handleSort = () => {
  getMenuList(true)
}

const loadMore = async () => {
  if (loadingMore.value || !hasMore.value) return

  loadingMore.value = true
  currentPage.value++

  try {
    const params = {
      page: currentPage.value,
      per_page: pageSize.value,
      category: selectedCategory.value === 'all' ? undefined : selectedCategory.value,
      keyword: searchQuery.value || undefined
    }

    const response = await menuAPI.getMenuList(params)
    menuItems.value.push(...(response.data.items || []))
    hasMore.value = menuItems.value.length < pagination.total

  } catch (error) {
    console.error('加载更多失败:', error)
    ElMessage.error('加载更多失败，请稍后重试')
    currentPage.value-- // 恢复页码
  } finally {
    loadingMore.value = false
  }
}

const resetFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = 'all'
  sortBy.value = 'default'
  getMenuList(true)
}

const handleAddToCart = async (item, quantity = 1) => {
  // 检查用户是否已登录
  if (!authStore.isAuthenticated) {
    ElMessageBox.confirm(
      '请先登录后再添加商品到购物车',
      '提示',
      {
        confirmButtonText: '去登录',
        cancelButtonText: '取消',
        type: 'info'
      }
    ).then(() => {
      // 跳转到登录页面
      authStore.setRedirectPath('/menu')
      // 这里可以调用路由跳转到登录页
    }).catch(() => {
      // 用户取消
    })
    return
  }

  try {
    await cartStore.addItem(item, quantity)
    ElMessage.success(`${item.name} 已添加到购物车`)
  } catch (error) {
    console.error('添加到购物车失败:', error)
    ElMessage.error('添加到购物车失败，请稍后重试')
  }
}

const handleViewDetail = (item) => {
  selectedItem.value = item
  detailDialogVisible.value = true
}

const handleAddToCartFromDetail = async () => {
  if (!selectedItem.value) return

  addingToCart.value = true

  try {
    await handleAddToCart(selectedItem.value)
    detailDialogVisible.value = false
  } finally {
    addingToCart.value = false
  }
}

const getCategoryLabel = (categoryValue) => {
  const category = categories.value.find(cat => cat.value === categoryValue)
  return category ? category.label : categoryValue
}

const getItemAnimationDelay = (itemId) => {
  // 为每个项目设置不同的动画延迟，创建波浪效果
  const index = menuItems.value.findIndex(item => item.id === itemId)
  return index * 50 // 每个项目延迟50ms
}

// 生命周期
onMounted(async () => {
  await Promise.all([
    getCategories(),
    getMenuList(true)
  ])
})
</script>

<style lang="scss" scoped>
.menu-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
  padding: 20px;
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

.filter-section {
  margin-bottom: 30px;

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

    .search-box {
      flex: 1;
      min-width: 250px;

      .search-input {
        max-width: 400px;
      }
    }

    .category-filter {
      flex: 2;
      min-width: 300px;

      :deep(.el-radio-group) {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
      }
    }

    .sort-options {
      min-width: 150px;
    }
  }
}

.menu-content {
  max-width: 1200px;
  margin: 0 auto;
}

.loading-container {
  padding: 40px;
}

.empty-state {
  padding: 60px 20px;
  text-align: center;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 25px;
  margin-bottom: 40px;

  .menu-item-wrapper {
    transform: translateY(0);
    transition: transform 0.3s ease;

    &:hover {
      transform: translateY(-5px);
    }
  }
}

.load-more {
  text-align: center;
  margin-top: 40px;

  .load-more-btn {
    padding: 12px 30px;
    font-size: 1rem;
    border-radius: 25px;
  }
}

.detail-dialog {
  :deep(.el-dialog) {
    border-radius: 12px;
  }

  .item-detail {
    display: flex;
    gap: 20px;
    margin-bottom: 20px;

    .detail-image {
      flex-shrink: 0;
      width: 200px;
      height: 200px;
      border-radius: 8px;
      overflow: hidden;

      img {
        width: 100%;
        height: 100%;
        object-fit: cover;
      }
    }

    .detail-info {
      flex: 1;

      h3 {
        margin: 0 0 15px 0;
        color: #2c3e50;
        font-size: 1.5rem;
      }

      .description {
        color: #7f8c8d;
        line-height: 1.6;
        margin-bottom: 20px;
      }

      .price-info {
        margin-bottom: 15px;

        .price {
          font-size: 1.8rem;
          font-weight: bold;
          color: #e74c3c;
        }

        .original-price {
          font-size: 1.2rem;
          color: #95a5a6;
          text-decoration: line-through;
          margin-left: 10px;
        }
      }

      .category-tag {
        margin-bottom: 20px;
      }
    }
  }

  .dialog-footer {
    .el-button {
      border-radius: 20px;
      padding: 10px 20px;
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .menu-page {
    padding: 15px;
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

    .search-box,
    .category-filter,
    .sort-options {
      width: 100%;
    }
  }

  .menu-grid {
    grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
    gap: 20px;
  }

  .item-detail {
    flex-direction: column;

    .detail-image {
      width: 100%;
      height: 250px;
    }
  }
}
</style>