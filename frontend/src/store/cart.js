import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export const useCartStore = defineStore('cart', () => {
  // 状态
  const items = ref([])
  const loading = ref(false)

  // 计算属性
  const itemCount = computed(() => {
    return items.value.reduce((total, item) => total + item.quantity, 0)
  })

  const totalPrice = computed(() => {
    return items.value.reduce((total, item) => total + item.subtotal, 0)
  })

  const isEmpty = computed(() => items.value.length === 0)

  // 获取购物车项
  const getItemById = (itemId) => {
    return items.value.find(item => item.id === itemId)
  }

  // 获取购物车项索引
  const getItemIndex = (itemId) => {
    return items.value.findIndex(item => item.id === itemId)
  }

  // 添加商品到购物车
  const addItem = (menuItem, quantity = 1) => {
    try {
      const existingItem = getItemById(menuItem.id)

      if (existingItem) {
        // 如果商品已存在，增加数量
        existingItem.quantity += quantity
        existingItem.subtotal = existingItem.quantity * existingItem.unit_price
      } else {
        // 如果商品不存在，添加新项
        items.value.push({
          id: menuItem.id,
          name: menuItem.name,
          price: menuItem.price,
          image_url: menuItem.image_url,
          category: menuItem.category,
          unit_price: menuItem.price,
          quantity: quantity,
          subtotal: menuItem.price * quantity,
          added_at: new Date().toISOString()
        })
      }

      // 保存到本地存储
      saveCartToStorage()
      return { success: true }
    } catch (error) {
      console.error('添加购物车失败:', error)
      return { success: false, error: error.message }
    }
  }

  // 更新购物车项数量
  const updateQuantity = (itemId, quantity) => {
    try {
      const item = getItemById(itemId)
      if (!item) {
        return { success: false, error: '商品不存在' }
      }

      if (quantity <= 0) {
        return removeItem(itemId)
      }

      item.quantity = quantity
      item.subtotal = quantity * item.unit_price

      saveCartToStorage()
      return { success: true }
    } catch (error) {
      console.error('更新购物车失败:', error)
      return { success: false, error: error.message }
    }
  }

  // 移除购物车项
  const removeItem = (itemId) => {
    try {
      const itemIndex = getItemIndex(itemId)
      if (itemIndex === -1) {
        return { success: false, error: '商品不存在' }
      }

      items.value.splice(itemIndex, 1)
      saveCartToStorage()
      return { success: true }
    } catch (error) {
      console.error('移除购物车项失败:', error)
      return { success: false, error: error.message }
    }
  }

  // 清空购物车
  const clearCart = () => {
    try {
      items.value = []
      saveCartToStorage()
      return { success: true }
    } catch (error) {
      console.error('清空购物车失败:', error)
      return { success: false, error: error.message }
    }
  }

  // 增加数量
  const increaseQuantity = (itemId) => {
    const item = getItemById(itemId)
    if (item) {
      return updateQuantity(itemId, item.quantity + 1)
    }
    return { success: false, error: '商品不存在' }
  }

  // 减少数量
  const decreaseQuantity = (itemId) => {
    const item = getItemById(itemId)
    if (item) {
      return updateQuantity(itemId, item.quantity - 1)
    }
    return { success: false, error: '商品不存在' }
  }

  // 获取购物车格式化数据（用于提交订单）
  const getCartData = () => {
    return items.value.map(item => ({
      menu_id: item.id,
      quantity: item.quantity,
      unit_price: item.unit_price
    }))
  }

  // 验证购物车
  const validateCart = () => {
    const errors = []

    if (items.value.length === 0) {
      errors.push('购物车为空')
      return { valid: false, errors }
    }

    items.value.forEach(item => {
      if (item.quantity <= 0) {
        errors.push(`${item.name} 数量无效`)
      }
    })

    return {
      valid: errors.length === 0,
      errors
    }
  }

  // 保存购物车到本地存储
  const saveCartToStorage = () => {
    try {
      localStorage.setItem('cart', JSON.stringify(items.value))
    } catch (error) {
      console.error('保存购物车失败:', error)
    }
  }

  // 从本地存储加载购物车
  const loadCartFromStorage = () => {
    try {
      const storedCart = localStorage.getItem('cart')
      if (storedCart) {
        items.value = JSON.parse(storedCart)
      }
    } catch (error) {
      console.error('加载购物车失败:', error)
      items.value = []
    }
  }

  // 获取购物车商品列表
  const getCartItems = () => {
    return items.value
  }

  // 获取购物车摘要信息
  const getCartSummary = () => {
    return {
      itemCount: itemCount.value,
      totalPrice: totalPrice.value,
      isEmpty: isEmpty.value,
      items: items.value
    }
  }

  // 初始化购物车
  const initCart = () => {
    loadCartFromStorage()
  }

  // 重置购物车（下单后调用）
  const resetCart = () => {
    clearCart()
  }

  return {
    // 状态
    items,
    loading,

    // 计算属性
    itemCount,
    totalPrice,
    isEmpty,

    // 方法
    addItem,
    removeItem,
    updateQuantity,
    increaseQuantity,
    decreaseQuantity,
    clearCart,
    validateCart,
    getCartData,
    getCartItems,
    getCartSummary,
    initCart,
    resetCart,
    saveCartToStorage,
    loadCartFromStorage
  }
})