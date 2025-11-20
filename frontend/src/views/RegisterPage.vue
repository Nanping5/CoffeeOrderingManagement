<template>
  <div class="register-page animate__animated animate__fadeIn">
    <div class="register-header">
      <h2>创建账户</h2>
      <p>加入我们，享受美味咖啡</p>
    </div>

    <el-form
      ref="registerFormRef"
      :model="registerForm"
      :rules="registerRules"
      class="register-form"
      @submit.prevent="handleRegister"
    >
      <el-form-item prop="username">
        <el-input
          v-model="registerForm.username"
          placeholder="用户名"
          size="large"
          :prefix-icon="User"
          clearable
        />
      </el-form-item>

      <el-form-item prop="email">
        <el-input
          v-model="registerForm.email"
          placeholder="邮箱地址"
          size="large"
          :prefix-icon="Message"
          clearable
        />
      </el-form-item>

      <el-form-item prop="phone">
        <el-input
          v-model="registerForm.phone"
          placeholder="手机号码（可选）"
          size="large"
          :prefix-icon="Phone"
          clearable
        />
      </el-form-item>

      <el-form-item prop="password">
        <el-input
          v-model="registerForm.password"
          type="password"
          placeholder="密码"
          size="large"
          :prefix-icon="Lock"
          show-password
        />
      </el-form-item>

      <el-form-item prop="confirmPassword">
        <el-input
          v-model="registerForm.confirmPassword"
          type="password"
          placeholder="确认密码"
          size="large"
          :prefix-icon="Lock"
          show-password
          @keyup.enter="handleRegister"
        />
      </el-form-item>

      <el-form-item>
        <el-checkbox v-model="registerForm.agreeTerms">
          我已阅读并同意
          <el-link type="primary" @click="showTermsDialog = true">
            服务条款
          </el-link>
          和
          <el-link type="primary" @click="showPrivacyDialog = true">
            隐私政策
          </el-link>
        </el-checkbox>
      </el-form-item>

      <el-form-item>
        <el-button
          type="primary"
          size="large"
          :loading="authStore.loading"
          :disabled="!registerForm.agreeTerms"
          @click="handleRegister"
          class="register-button"
        >
          {{ authStore.loading ? '注册中...' : '注册' }}
        </el-button>
      </el-form-item>
    </el-form>

    <div class="register-footer">
      <p>
        已有账户？
        <router-link to="/login" class="login-link">
          立即登录
        </router-link>
      </p>
    </div>

    <!-- 服务条款对话框 -->
    <el-dialog
      v-model="showTermsDialog"
      title="服务条款"
      width="500px"
      :show-close="false"
    >
      <div class="terms-content">
        <h4>1. 服务说明</h4>
        <p>欢迎使用咖啡点餐系统。本服务为用户提供便捷的咖啡订购体验。</p>

        <h4>2. 用户责任</h4>
        <p>用户需提供真实、准确的信息，并对账户安全负责。</p>

        <h4>3. 订单规定</h4>
        <p>用户下单后请及时付款，我们将在确认后尽快准备您的订单。</p>

        <h4>4. 隐私保护</h4>
        <p>我们将严格保护您的个人信息，不会向第三方泄露。</p>
      </div>
      <template #footer>
        <el-button @click="showTermsDialog = false">确定</el-button>
      </template>
    </el-dialog>

    <!-- 隐私政策对话框 -->
    <el-dialog
      v-model="showPrivacyDialog"
      title="隐私政策"
      width="500px"
      :show-close="false"
    >
      <div class="privacy-content">
        <h4>1. 信息收集</h4>
        <p>我们收集您的姓名、邮箱、电话等基本信息，用于提供更好的服务。</p>

        <h4>2. 信息使用</h4>
        <p>您的信息仅用于订单处理、客户服务和系统改进。</p>

        <h4>3. 信息保护</h4>
        <p>我们采用行业标准的加密技术保护您的个人信息。</p>

        <h4>4. Cookie使用</h4>
        <p>网站使用Cookie来提升用户体验，您可以选择禁用Cookie。</p>
      </div>
      <template #footer>
        <el-button @click="showPrivacyDialog = false">确定</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Phone } from '@element-plus/icons-vue'
import { useAuthStore } from '@/store/auth'

const router = useRouter()
const authStore = useAuthStore()

// 表单引用
const registerFormRef = ref(null)

// 对话框显示状态
const showTermsDialog = ref(false)
const showPrivacyDialog = ref(false)

// 注册表单数据
const registerForm = reactive({
  username: '',
  email: '',
  phone: '',
  password: '',
  confirmPassword: '',
  agreeTerms: false
})

// 表单验证规则
const registerRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度在3-20个字符', trigger: 'blur' },
    { pattern: /^[a-zA-Z0-9_]+$/, message: '用户名只能包含字母、数字和下划线', trigger: 'blur' }
  ],
  email: [
    { required: true, message: '请输入邮箱地址', trigger: 'blur' },
    { type: 'email', message: '请输入正确的邮箱格式', trigger: 'blur' }
  ],
  phone: [
    { pattern: /^1[3-9]\d{9}$/, message: '请输入正确的手机号码', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度在6-20个字符', trigger: 'blur' },
    { pattern: /^(?=.*[a-zA-Z])(?=.*\d).+$/, message: '密码必须包含字母和数字', trigger: 'blur' }
  ],
  confirmPassword: [
    { required: true, message: '请确认密码', trigger: 'blur' },
    {
      validator: (rule, value, callback) => {
        if (value !== registerForm.password) {
          callback(new Error('两次输入的密码不一致'))
        } else {
          callback()
        }
      },
      trigger: 'blur'
    }
  ]
}

// 处理注册
const handleRegister = async () => {
  if (!registerFormRef.value) return

  try {
    // 表单验证
    const valid = await registerFormRef.value.validate()
    if (!valid) return

    // 检查是否同意条款
    if (!registerForm.agreeTerms) {
      ElMessage.warning('请先同意服务条款和隐私政策')
      return
    }

    // 调用注册API
    const result = await authStore.register({
      username: registerForm.username,
      email: registerForm.email,
      password: registerForm.password,
      phone: registerForm.phone
    })

    if (result.success) {
      ElMessage.success('注册成功！')
      // 注册成功后自动登录并跳转到首页
      router.push('/menu')
    } else {
      ElMessage.error(result.errors?.join(', ') || '注册失败')
    }
  } catch (error) {
    console.error('注册错误:', error)
    ElMessage.error('注册失败，请稍后重试')
  }
}
</script>

<style lang="scss" scoped>
.register-page {
  width: 100%;
  max-width: 450px;
}

.register-header {
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

.register-form {
  .el-form-item {
    margin-bottom: $spacing-lg;
  }

  .register-button {
    width: 100%;
    height: 48px;
    font-size: var(--font-size-lg);
    font-weight: 600;
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
    border: none;
    border-radius: $border-radius-medium;

    &:hover:not(:disabled) {
      background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-dark) 100%);
    }

    &:disabled {
      opacity: 0.6;
      cursor: not-allowed;
    }
  }

  .el-checkbox {
    .el-link {
      margin: 0 2px;
      font-weight: 500;
    }
  }
}

.register-footer {
  text-align: center;
  margin-top: $spacing-lg;

  p {
    color: var(--text-secondary);
    font-size: var(--font-size-sm);

    .login-link {
      color: var(--primary-color);
      text-decoration: none;
      font-weight: 500;

      &:hover {
        text-decoration: underline;
      }
    }
  }
}

.terms-content,
.privacy-content {
  max-height: 300px;
  overflow-y: auto;
  padding-right: $spacing-sm;

  h4 {
    font-size: var(--font-size-md);
    color: var(--text-primary);
    margin: $spacing-md 0 $spacing-sm 0;

    &:first-child {
      margin-top: 0;
    }
  }

  p {
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: $spacing-md;
    font-size: var(--font-size-sm);
  }
}

// 响应式设计
@include mobile {
  .register-page {
    max-width: 100%;
  }
}

// 自定义滚动条样式
.terms-content::-webkit-scrollbar,
.privacy-content::-webkit-scrollbar {
  width: 4px;
}

.terms-content::-webkit-scrollbar-track,
.privacy-content::-webkit-scrollbar-track {
  background: var(--background-color);
}

.terms-content::-webkit-scrollbar-thumb,
.privacy-content::-webkit-scrollbar-thumb {
  background: var(--primary-light);
  border-radius: 2px;
}

.terms-content::-webkit-scrollbar-thumb:hover,
.privacy-content::-webkit-scrollbar-thumb:hover {
  background: var(--primary-color);
}
</style>