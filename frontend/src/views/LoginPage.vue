<template>
  <div class="login-page animate__animated animate__fadeIn">
    <div class="login-header">
      <h2>欢迎回来</h2>
      <p>登录您的账户开始点餐</p>
    </div>

    <el-form
      ref="loginFormRef"
      :model="loginForm"
      :rules="loginRules"
      class="login-form"
      @submit.prevent="handleLogin"
    >
      <el-form-item prop="username">
        <el-input
          v-model="loginForm.username"
          placeholder="用户名或邮箱"
          size="large"
          :prefix-icon="User"
          clearable
          @keyup.enter="handleLogin"
        />
      </el-form-item>

      <el-form-item prop="password">
        <el-input
          v-model="loginForm.password"
          type="password"
          placeholder="密码"
          size="large"
          :prefix-icon="Lock"
          show-password
          @keyup.enter="handleLogin"
        />
      </el-form-item>

      <el-form-item>
        <div class="login-options">
          <el-checkbox v-model="loginForm.rememberMe">
            记住我
          </el-checkbox>
          <el-link type="primary" @click="showForgotPassword = true">
            忘记密码？
          </el-link>
        </div>
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          size="large"
          :loading="authStore.loading"
          @click="handleLogin"
          class="login-button"
        >
          {{ authStore.loading ? '登录中...' : '登录' }}
        </el-button>
      </el-form-item>
    </el-form>

    <div class="login-footer">
      <p>
        还没有账户？
        <router-link to="/register" class="register-link">
          立即注册
        </router-link>
      </p>
    </div>

    <!-- 分割线 -->
    <div class="divider">
      <span>或</span>
    </div>

    <!-- 演示账户信息 -->
    <div class="demo-accounts">
      <h4>演示账户</h4>
      <div class="demo-account-item">
        <el-tag type="primary">用户</el-tag>
        <span>用户名: testuser</span>
        <span>密码: admin123</span>
      </div>
      <div class="demo-account-item">
        <el-tag type="danger">管理员</el-tag>
        <span>用户名: admin</span>
        <span>密码: admin123</span>
      </div>
    </div>

    <!-- 忘记密码对话框 -->
    <el-dialog
      v-model="showForgotPassword"
      title="重置密码"
      width="400px"
      :show-close="false"
    >
      <p class="forgot-password-tip">
        请联系管理员重置密码，或发送邮件至 support@coffee.com
      </p>
      <template #footer>
        <el-button @click="showForgotPassword = false">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

// 表单引用
const loginFormRef = ref(null)

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: '',
  rememberMe: false
})

// 忘记密码对话框
const showForgotPassword = ref(false)

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名或邮箱', trigger: 'blur' },
    { min: 3, message: '用户名至少3个字符', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, message: '密码至少6个字符', trigger: 'blur' }
  ]
}

// 处理登录
const handleLogin = async () => {
  if (!loginFormRef.value) return

  try {
    // 表单验证
    const valid = await loginFormRef.value.validate()
    if (!valid) return

    // 调用登录API
    const result = await authStore.login({
      username: loginForm.username,
      password: loginForm.password
    })

    if (result.success) {
      ElMessage.success('登录成功！')

      // 记住我功能
      if (loginForm.rememberMe) {
        localStorage.setItem('rememberMe', 'true')
        localStorage.setItem('username', loginForm.username)
      } else {
        localStorage.removeItem('rememberMe')
        localStorage.removeItem('username')
      }

      // 跳转到重定向页面或首页
      const redirect = route.query.redirect || '/menu'
      router.push(redirect)
    } else {
      ElMessage.error(result.errors?.join(', ') || '登录失败')
    }
  } catch (error) {
    console.error('登录错误:', error)
    ElMessage.error('登录失败，请稍后重试')
  }
}

// 初始化记住的用户名
const initRememberMe = () => {
  const rememberMe = localStorage.getItem('rememberMe')
  const username = localStorage.getItem('username')

  if (rememberMe === 'true' && username) {
    loginForm.rememberMe = true
    loginForm.username = username
  }
}

// 组件挂载时初始化
initRememberMe()
</script>

<style lang="scss" scoped>
.login-page {
  width: 100%;
  max-width: 400px;
}

.login-header {
  text-align: center;
  margin-bottom: $spacing-xl;

  h2 {
    font-size: var(--font-size-xxl);
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: $spacing-sm;
  }

  p {
    color: var(--text-secondary);
    font-size: var(--font-size-md);
  }
}

.login-form {
  .el-form-item {
    margin-bottom: $spacing-lg;
  }

  .login-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
  }

  .login-button {
    width: 100%;
    height: 48px;
    font-size: var(--font-size-lg);
    font-weight: 600;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
    border: none;
    border-radius: $border-radius-medium;

    &:hover {
      background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-dark) 100%);
    }
  }
}

.login-footer {
  text-align: center;
  margin-top: $spacing-lg;

  p {
    color: var(--text-secondary);
    font-size: var(--font-size-sm);

    .register-link {
      color: var(--primary-color);
      text-decoration: none;
      font-weight: 500;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}

.divider {
  display: flex;
  align-items: center;
  margin: $spacing-lg 0;
  color: var(--text-light);

  &::before,
  &::after {
    content: '';
    flex: 1;
    height: 1px;
    background-color: var(--border-color);
  }

  span {
    padding: 0 $spacing-md;
    font-size: var(--font-size-sm);
  }
}

.demo-accounts {
  margin-top: $spacing-lg;
  padding: $spacing-md;
  background-color: var(--accent-color);
  border-radius: $border-radius-medium;
  border: 1px solid var(--border-color);

  h4 {
    font-size: var(--font-size-md);
    color: var(--text-primary);
    margin-bottom: $spacing-sm;
    text-align: center;
  }

  .demo-account-item {
    display: flex;
    align-items: center;
    gap: $spacing-sm;
    margin-bottom: $spacing-xs;
    font-size: var(--font-size-xs);
    color: var(--text-secondary);

    &:last-child {
      margin-bottom: 0;
    }

    .el-tag {
      flex-shrink: 0;
    }

    span {
      &:nth-child(2),
      &:nth-child(3) {
        flex: 1;
        @include text-ellipsis;
      }
    }
  }
}

.forgot-password-tip {
  color: var(--text-secondary);
  line-height: 1.6;
  margin-bottom: 0;
}

// 响应式设计
@include mobile {
  .login-page {
    max-width: 100%;
  }

  .login-options {
    flex-direction: column;
    gap: $spacing-sm;
    align-items: flex-start;
  }
}
</style>