import { ref, onMounted, onUnmounted, nextTick } from 'vue'
import animations, { getAnimationDelay } from '@/utils/animations'

/**
 * 动画组合式函数
 * 提供常用的动画效果和交互功能
 */
export function useAnimation() {
  const animationClass = ref('')
  const isAnimating = ref(false)

  /**
   * 播放动画
   * @param {string} animationName - 动画名称
   * @param {number} duration - 动画持续时间
   */
  const playAnimation = (animationName, duration = 1000) => {
    animationClass.value = `animate__animated ${animationName}`
    isAnimating.value = true

    setTimeout(() => {
      animationClass.value = ''
      isAnimating.value = false
    }, duration)
  }

  /**
   * 播放页面进入动画
   * @param {string} type - 动画类型
   */
  const playPageAnimation = (type = 'fadeInUp') => {
    const animationConfig = animations.pageAnimations[type]
    if (animationConfig) {
      playAnimation(animationConfig.enterActiveClass.replace('animate__animated ', ''), 1000)
    }
  }

  /**
   * 播放按钮点击动画
   */
  const playButtonClick = () => {
    playAnimation('headShake', 500)
  }

  /**
   * 播放成功动画
   */
  const playSuccess = () => {
    playAnimation('bounceIn', 800)
  }

  /**
   * 播放错误动画
   */
  const playError = () => {
    playAnimation('shakeX', 500)
  }

  /**
   * 播放加载动画
   */
  const playLoading = () => {
    animationClass.value = 'animate__animated animate__pulse infinite'
    isAnimating.value = true
  }

  /**
   * 停止动画
   */
  const stopAnimation = () => {
    animationClass.value = ''
    isAnimating.value = false
  }

  return {
    animationClass,
    isAnimating,
    playAnimation,
    playPageAnimation,
    playButtonClick,
    playSuccess,
    playError,
    playLoading,
    stopAnimation
  }
}

/**
 * 滚动动画组合式函数
 * 实现滚动触发动画效果
 */
export function useScrollAnimation() {
  const visibleElements = ref(new Set())
  const observer = ref(null)

  /**
   * 创建交叉观察器
   */
  const createObserver = () => {
    observer.value = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            visibleElements.value.add(entry.target)
            entry.target.classList.add('animate__animated', 'animate__fadeInUp')
          }
        })
      },
      {
        threshold: 0.1,
        rootMargin: '50px'
      }
    )
  }

  /**
   * 观察元素
   * @param {HTMLElement} element - 要观察的元素
   * @param {number} delay - 动画延迟时间
   */
  const observeElement = (element, delay = 0) => {
    if (!observer.value || !element) return

    if (delay > 0) {
      element.style.animationDelay = `${delay}ms`
    }

    observer.value.observe(element)
  }

  /**
   * 观察多个元素
   * @param {NodeList|Array} elements - 要观察的元素列表
   * @param {number} baseDelay - 基础延迟时间
   */
  const observeElements = (elements, baseDelay = 100) => {
    if (!elements) return

    elements.forEach((element, index) => {
      observeElement(element, index * baseDelay)
    })
  }

  /**
   * 停止观察元素
   * @param {HTMLElement} element - 要停止观察的元素
   */
  const unobserveElement = (element) => {
    if (observer.value && element) {
      observer.value.unobserve(element)
    }
  }

  /**
   * 清理观察器
   */
  const cleanup = () => {
    if (observer.value) {
      observer.value.disconnect()
      observer.value = null
    }
    visibleElements.value.clear()
  }

  onMounted(() => {
    createObserver()
  })

  onUnmounted(() => {
    cleanup()
  })

  return {
    visibleElements,
    observeElement,
    observeElements,
    unobserveElement,
    cleanup
  }
}

/**
 * 列表动画组合式函数
 * 实现列表项的进入/离开动画
 */
export function useListAnimation() {
  const listItems = ref([])
  const enteringItems = ref(new Set())
  const leavingItems = ref(new Set())

  /**
   * 添加列表项
   * @param {any} item - 列表项数据
   * @param {number} index - 插入位置
   */
  const addItem = (item, index = listItems.value.length) => {
    listItems.value.splice(index, 0, item)
    enteringItems.value.add(item)

    setTimeout(() => {
      enteringItems.value.delete(item)
    }, 600)
  }

  /**
   * 移除列表项
   * @param {any} item - 要移除的列表项
   */
  const removeItem = (item) => {
    leavingItems.value.add(item)

    setTimeout(() => {
      const index = listItems.value.findIndex(i => i === item)
      if (index > -1) {
        listItems.value.splice(index, 1)
      }
      leavingItems.value.delete(item)
    }, 300)
  }

  /**
   * 获取列表项的动画类名
   * @param {any} item - 列表项
   * @returns {string} 动画类名
   */
  const getItemAnimationClass = (item) => {
    if (enteringItems.value.has(item)) {
      return 'animate__animated animate__fadeInUp'
    }
    if (leavingItems.value.has(item)) {
      return 'animate__animated animate__fadeOutDown'
    }
    return ''
  }

  /**
   * 批量添加列表项
   * @param {Array} items - 要添加的列表项数组
   */
  const addItems = (items) => {
    items.forEach((item, index) => {
      addItem(item, index)
    })
  }

  /**
   * 清空列表
   */
  const clearList = () => {
    listItems.value.forEach(item => {
      leavingItems.value.add(item)
    })

    setTimeout(() => {
      listItems.value = []
      leavingItems.value.clear()
    }, 300)
  }

  return {
    listItems,
    enteringItems,
    leavingItems,
    addItem,
    removeItem,
    getItemAnimationClass,
    addItems,
    clearList
  }
}

/**
 * 购物车动画组合式函数
 * 专门处理购物车相关的动画效果
 */
export function useCartAnimation() {
  const cartIconClass = ref('')
  const isCartPulsing = ref(false)

  /**
   * 播放添加到购物车动画
   * @param {string} productId - 商品ID
   */
  const playAddToCartAnimation = (productId) => {
    // 播放购物车图标脉冲动画
    isCartPulsing.value = true
    cartIconClass.value = 'animate__animated animate__pulse'

    // 播放商品飞入动画（需要配合CSS实现）
    const productElement = document.querySelector(`[data-product-id="${productId}"]`)
    if (productElement) {
      productElement.classList.add('animate__animated', 'animate__bounceOut')

      setTimeout(() => {
        productElement.classList.remove('animate__animated', 'animate__bounceOut')
      }, 600)
    }

    setTimeout(() => {
      isCartPulsing.value = false
      cartIconClass.value = ''
    }, 1000)
  }

  /**
   * 播放购物车数量变化动画
   */
  const playQuantityChangeAnimation = () => {
    cartIconClass.value = 'animate__animated animate__rubberBand'

    setTimeout(() => {
      cartIconClass.value = ''
    }, 600)
  }

  /**
   * 播放购物车震动动画
   */
  const playCartShakeAnimation = () => {
    cartIconClass.value = 'animate__animated animate__shakeX'

    setTimeout(() => {
      cartIconClass.value = ''
    }, 500)
  }

  return {
    cartIconClass,
    isCartPulsing,
    playAddToCartAnimation,
    playQuantityChangeAnimation,
    playCartShakeAnimation
  }
}

/**
 * 页面过渡动画组合式函数
 * 处理路由切换时的页面动画
 */
export function usePageTransition() {
  const transitionName = ref('fade')
  const isTransitioning = ref(false)

  /**
   * 设置页面过渡效果
   * @param {string} from - 来源路由
   * @param {string} to - 目标路由
   */
  const setPageTransition = (from, to) => {
    isTransitioning.value = true

    // 根据路由类型设置不同的过渡效果
    const transitions = {
      // 用户页面之间的过渡
      'menu-to-cart': 'slide-left',
      'cart-to-menu': 'slide-right',
      'menu-to-orders': 'slide-left',
      'orders-to-menu': 'slide-right',
      'menu-to-profile': 'slide-up',
      'profile-to-menu': 'slide-down',

      // 管理页面之间的过渡
      'admin-to-menu': 'slide-right',
      'menu-to-admin': 'slide-left',

      // 认证页面过渡
      'login-to-register': 'slide-left',
      'register-to-login': 'slide-right',

      // 默认过渡
      'default': 'fade'
    }

    const transitionKey = `${from}-to-${to}`
    transitionName.value = transitions[transitionKey] || transitions['default']

    setTimeout(() => {
      isTransitioning.value = false
    }, 300)
  }

  /**
   * 获取过渡类名
   * @returns {string} 过渡类名
   */
  const getTransitionClass = () => {
    return `transition-${transitionName.value}`
  }

  return {
    transitionName,
    isTransitioning,
    setPageTransition,
    getTransitionClass
  }
}

// 导出所有动画组合式函数
export default {
  useAnimation,
  useScrollAnimation,
  useListAnimation,
  useCartAnimation,
  usePageTransition
}