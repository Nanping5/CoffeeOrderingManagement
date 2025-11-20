import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/store/auth'

// 创建axios实例
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
api.interceptors.request.use(
  (config) => {
    // 添加token到请求头
    const authStore = useAuthStore()
    const token = authStore.token
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    console.error('请求配置错误:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
api.interceptors.response.use(
  (response) => {
    // 统一处理响应数据
    const { data } = response
    if (data.success === false) {
      ElMessage.error(data.message || data.errors?.join(', ') || '请求失败')
      return Promise.reject(new Error(data.message || '请求失败'))
    }
    return data
  },
  (error) => {
    console.error('响应错误:', error)

    const authStore = useAuthStore()

    // 处理不同的HTTP状态码
    if (error.response) {
      const { status, data } = error.response

      switch (status) {
        case 401:
          // 未授权，清除token并跳转到登录页
          ElMessage.error('登录已过期，请重新登录')
          authStore.logout()
          // 这里可以添加路由跳转逻辑
          break
        case 403:
          ElMessage.error('权限不足')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 422:
          // 表单验证错误
          const errors = data.errors || []
          if (Array.isArray(errors)) {
            ElMessage.error(errors.join(', '))
          } else {
            ElMessage.error(data.message || '请求参数错误')
          }
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(data.message || `请求失败 (${status})`)
      }
    } else if (error.request) {
      // 网络错误
      ElMessage.error('网络连接失败，请检查网络设置')
    } else {
      // 其他错误
      ElMessage.error(error.message || '请求配置错误')
    }

    return Promise.reject(error)
  }
)

// 请求方法封装
const request = {
  // GET请求
  get(url, params = {}) {
    return api.get(url, { params })
  },

  // POST请求
  post(url, data = {}) {
    return api.post(url, data)
  },

  // PUT请求
  put(url, data = {}) {
    return api.put(url, data)
  },

  // PATCH请求
  patch(url, data = {}) {
    return api.patch(url, data)
  },

  // DELETE请求
  delete(url) {
    return api.delete(url)
  },

  // 文件上传
  upload(url, formData, onProgress) {
    return api.post(url, formData, {
      headers: {
        'Content-Type': 'multipart/form-data'
      },
      onUploadProgress: (progressEvent) => {
        if (onProgress) {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          )
          onProgress(progress)
        }
      }
    })
  },

  // 下载文件
  download(url, params = {}, filename) {
    return api.get(url, {
      params,
      responseType: 'blob'
    }).then((response) => {
      // 创建下载链接
      const blob = new Blob([response])
      const downloadUrl = window.URL.createObjectURL(blob)
      const link = document.createElement('a')
      link.href = downloadUrl
      link.download = filename || 'download'
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
      window.URL.revokeObjectURL(downloadUrl)
    })
  }
}

export default request