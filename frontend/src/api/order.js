import request from './index'

export default {
  // 创建订单
  createOrder(orderData) {
    return request.post('/orders', orderData)
  },

  // 获取订单列表
  getOrderList(params = {}) {
    return request.get('/orders', params)
  },

  // 获取订单详情
  getOrderDetail(id) {
    return request.get(`/orders/${id}`)
  },

  // 获取我的订单
  getMyOrders(params = {}) {
    return request.get('/orders/my', params)
  },

  // 取消订单
  cancelOrder(id) {
    return request.put(`/orders/${id}/cancel`)
  },

  // 更新订单状态（管理员）
  updateOrderStatus(id, status) {
    return request.put(`/orders/${id}/status`, { status })
  },

  // 获取订单统计信息（管理员）
  getOrderStatistics(params = {}) {
    return request.get('/orders/statistics', params)
  },

  // 获取每日销售数据（管理员）
  getDailySales(params = {}) {
    return request.get('/orders/sales/daily', params)
  },

  // 获取订单数量统计（管理员）
  getOrderCount() {
    return request.get('/orders/count')
  },

  // 获取最近订单（管理员）
  getRecentOrders(params = {}) {
    return request.get('/orders/recent', params)
  },

  // 根据状态获取订单
  getOrdersByStatus(status, params = {}) {
    return request.get(`/orders/status/${status}`, params)
  },

  // 搜索订单（管理员）
  searchOrders(params) {
    return request.get('/orders/search', params)
  }
}