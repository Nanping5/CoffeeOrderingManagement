/**
 * 动画效果工具函数
 * 基于Animate.css提供常用的动画效果配置
 */

// 动画延迟配置
export const animationDelays = {
  fast: '100ms',
  normal: '300ms',
  slow: '500ms',
  slower: '800ms'
}

// 页面进入动画
export const pageAnimations = {
  // 从上方淡入
  fadeInDown: {
    enterActiveClass: 'animate__animated animate__fadeInDown',
    leaveActiveClass: 'animate__animated animate__fadeOutUp'
  },

  // 从下方淡入
  fadeInUp: {
    enterActiveClass: 'animate__animated animate__fadeInUp',
    leaveActiveClass: 'animate__animated animate__fadeOutDown'
  },

  // 从左侧滑入
  slideInLeft: {
    enterActiveClass: 'animate__animated animate__slideInLeft',
    leaveActiveClass: 'animate__animated animate__slideOutLeft'
  },

  // 从右侧滑入
  slideInRight: {
    enterActiveClass: 'animate__animated animate__slideInRight',
    leaveActiveClass: 'animate__animated animate__slideOutRight'
  },

  // 缩放淡入
  zoomIn: {
    enterActiveClass: 'animate__animated animate__zoomIn',
    leaveActiveClass: 'animate__animated animate__zoomOut'
  },

  // 弹跳进入
  bounceIn: {
    enterActiveClass: 'animate__animated animate__bounceIn',
    leaveActiveClass: 'animate__animated animate__bounceOut'
  }
}

// 列表项动画
export const listAnimations = {
  // 淡入效果
  fadeIn: {
    enterActiveClass: 'animate__animated animate__fadeIn',
    leaveActiveClass: 'animate__animated animate__fadeOut'
  },

  // 从左到右依次进入
  slideInLeftSequential: {
    enterActiveClass: 'animate__animated animate__slideInLeft',
    leaveActiveClass: 'animate__animated animate__slideOutLeft'
  },

  // 弹跳进入
  bounceIn: {
    enterActiveClass: 'animate__animated animate__bounceIn',
    leaveActiveClass: 'animate__animated animate__bounceOut'
  },

  // 从下方滑入
  slideInUp: {
    enterActiveClass: 'animate__animated animate__slideInUp',
    leaveActiveClass: 'animate__animated animate__slideOutDown'
  }
}

// 卡片动画
export const cardAnimations = {
  // 悬停效果
  hover: {
    enterActiveClass: 'animate__animated animate__pulse',
    leaveActiveClass: ''
  },

  // 点击效果
  click: {
    enterActiveClass: 'animate__animated animate__rubberBand',
    leaveActiveClass: ''
  },

  // 加载效果
  loading: {
    enterActiveClass: 'animate__animated animate__fadeIn',
    leaveActiveClass: ''
  }
}

// 按钮动画
export const buttonAnimations = {
  // 悬停脉冲
  hoverPulse: {
    enterActiveClass: 'animate__animated animate__pulse infinite',
    leaveActiveClass: ''
  },

  // 点击震动
  clickShake: {
    enterActiveClass: 'animate__animated animate__headShake',
    leaveActiveClass: ''
  },

  // 加载旋转
  loading: {
    enterActiveClass: 'animate__animated animate__rotateIn',
    leaveActiveClass: 'animate__animated animate__rotateOut'
  }
}

// 通知动画
export const notificationAnimations = {
  // 从右侧滑入
  slideInRight: {
    enterActiveClass: 'animate__animated animate__slideInRight',
    leaveActiveClass: 'animate__animated animate__slideOutRight'
  },

  // 从上方弹入
  bounceInDown: {
    enterActiveClass: 'animate__animated animate__bounceInDown',
    leaveActiveClass: 'animate__animated animate__bounceOutUp'
  },

  // 闪光提醒
  flash: {
    enterActiveClass: 'animate__animated animate__flash',
    leaveActiveClass: 'animate__animated animate__fadeOut'
  }
}

// 模态框动画
export const modalAnimations = {
  // 缩放进入
  zoomIn: {
    enterActiveClass: 'animate__animated animate__zoomIn',
    leaveActiveClass: 'animate__animated animate__zoomOut'
  },

  // 从上方弹入
  bounceInDown: {
    enterActiveClass: 'animate__animated animate__bounceInDown',
    leaveActiveClass: 'animate__animated animate__bounceOutUp'
  },

  // 淡入缩放
  fadeInScale: {
    enterActiveClass: 'animate__animated animate__fadeInDownBig',
    leaveActiveClass: 'animate__animated animate__fadeOutUpBig'
  }
}

// 购物车动画
export const cartAnimations = {
  // 添加商品
  add: {
    enterActiveClass: 'animate__animated animate__bounceIn',
    leaveActiveClass: ''
  },

  // 移除商品
  remove: {
    enterActiveClass: 'animate__animated animate__fadeOutLeft',
    leaveActiveClass: ''
  },

  // 购物车图标脉冲
  iconPulse: {
    enterActiveClass: 'animate__animated animate__pulse',
    leaveActiveClass: ''
  },

  // 数量变化
  quantityChange: {
    enterActiveClass: 'animate__animated animate__rubberBand',
    leaveActiveClass: ''
  }
}

// 加载动画
export const loadingAnimations = {
  // 淡入
  fadeIn: {
    enterActiveClass: 'animate__animated animate__fadeIn',
    leaveActiveClass: 'animate__animated animate__fadeOut'
  },

  // 旋转加载
  spin: {
    enterActiveClass: 'animate__animated animate__rotateIn',
    leaveActiveClass: 'animate__animated animate__rotateOut'
  },

  // 脉冲加载
  pulse: {
    enterActiveClass: 'animate__animated animate__pulse infinite',
    leaveActiveClass: ''
  }
}

/**
 * 获取动画延迟样式
 * @param {number} index - 元素索引
 * @param {number} delay - 基础延迟时间（毫秒）
 * @returns {string} 动画延迟时间
 */
export const getAnimationDelay = (index, delay = 100) => {
  return `${index * delay}ms`
}

/**
 * 获取随机动画效果
 * @param {Array} animations - 动画列表
 * @returns {Object} 随机动画配置
 */
export const getRandomAnimation = (animations) => {
  const keys = Object.keys(animations)
  const randomKey = keys[Math.floor(Math.random() * keys.length)]
  return animations[randomKey]
}

/**
 * 创建动画过渡配置
 * @param {Object} config - 动画配置
 * @param {number} duration - 动画持续时间（毫秒）
 * @returns {Object} Vue transition配置
 */
export const createTransition = (config, duration = 300) => {
  return {
    ...config,
    duration,
    mode: 'out-in'
  }
}

/**
 * 获取页面切换动画配置
 * @param {string} fromRoute - 来源路由名称
 * @param {string} toRoute - 目标路由名称
 * @returns {Object} 动画配置
 */
export const getPageTransition = (fromRoute, toRoute) => {
  // 根据路由类型返回不同的动画效果
  const routeTypes = {
    'Menu': 'fadeInUp',
    'Cart': 'slideInRight',
    'Orders': 'slideInLeft',
    'Profile': 'fadeInDown',
    'Login': 'zoomIn',
    'Register': 'zoomIn',
    'AdminDashboard': 'bounceIn',
    'AdminMenu': 'slideInRight',
    'AdminOrders': 'slideInLeft',
    'AdminUsers': 'fadeInDown'
  }

  const getAnimationType = (routeName) => {
    return routeTypes[routeName] || 'fadeIn'
  }

  return {
    enterActiveClass: `animate__animated animate__${getAnimationType(toRoute)}`,
    leaveActiveClass: `animate__animated animate__fadeOut`
  }
}

/**
 * 列表项交错动画配置
 * @param {number} count - 列表项数量
 * @param {number} baseDelay - 基础延迟时间
 * @returns {Array} 动画延迟数组
 */
export const getStaggeredAnimationDelays = (count, baseDelay = 50) => {
  return Array.from({ length: count }, (_, index) => ({
    delay: `${index * baseDelay}ms`,
    animation: 'animate__animated animate__fadeInUp'
  }))
}

// 动画工具函数集合
export default {
  // 动画延迟
  animationDelays,

  // 各类动画配置
  pageAnimations,
  listAnimations,
  cardAnimations,
  buttonAnimations,
  notificationAnimations,
  modalAnimations,
  cartAnimations,
  loadingAnimations,

  // 工具函数
  getAnimationDelay,
  getRandomAnimation,
  createTransition,
  getPageTransition,
  getStaggeredAnimationDelays
}