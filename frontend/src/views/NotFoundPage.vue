<template>
  <div class="not-found-page">
    <div class="not-found-content animate__animated animate__fadeIn">
      <!-- 404图片或图标 -->
      <div class="not-found-image">
        <el-icon class="not-found-icon">
          <QuestionFilled />
        </el-icon>
      </div>

      <!-- 错误信息 -->
      <div class="not-found-info">
        <h1 class="error-code">404</h1>
        <h2 class="error-title">页面不存在</h2>
        <p class="error-description">
          抱歉，您访问的页面不存在或已被移动。
        </p>
      </div>

      <!-- 操作按钮 -->
      <div class="not-found-actions">
        <el-button
          type="primary"
          size="large"
          @click="goHome"
          class="home-button"
        >
          <el-icon><House /></el-icon>
          返回首页
        </el-button>

        <el-button
          size="large"
          @click="goBack"
          class="back-button"
        >
          <el-icon><ArrowLeft /></el-icon>
          返回上页
        </el-button>
      </div>

      <!-- 快速导航 -->
      <div class="quick-nav">
        <h3>您可以尝试：</h3>
        <div class="quick-links">
          <router-link to="/menu" class="quick-link">
            <el-icon><Coffee /></el-icon>
            浏览菜单
          </router-link>
          <router-link to="/orders" class="quick-link">
            <el-icon><Document /></el-icon>
            查看订单
          </router-link>
          <router-link to="/profile" class="quick-link">
            <el-icon><User /></el-icon>
            个人中心
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { QuestionFilled, House, ArrowLeft, Coffee, Document, User } from '@element-plus/icons-vue'

const router = useRouter()

// 返回首页
const goHome = () => {
  router.push('/menu')
}

// 返回上一页
const goBack = () => {
  if (window.history.length > 1) {
    router.go(-1)
  } else {
    goHome()
  }
}
</script>

<style lang="scss" scoped>
.not-found-page {
  min-height: calc(100vh - 140px);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: $spacing-xl;
}

.not-found-content {
  text-align: center;
  max-width: 600px;
  width: 100%;
}

.not-found-image {
  margin-bottom: $spacing-xl;

  .not-found-icon {
    font-size: 120px;
    color: var(--primary-light);
    opacity: 0.8;
  }
}

.not-found-info {
  margin-bottom: $spacing-xl;

  .error-code {
    font-size: 8rem;
    font-weight: 700;
    color: var(--primary-color);
    margin-bottom: $spacing-md;
    line-height: 1;
  }

  .error-title {
    font-size: var(--font-size-xxl);
    color: var(--text-primary);
    margin-bottom: $spacing-md;
    font-weight: 600;
  }

  .error-description {
    font-size: var(--font-size-lg);
    color: var(--text-secondary);
    line-height: 1.6;
    margin-bottom: 0;
  }
}

.not-found-actions {
  display: flex;
  justify-content: center;
  gap: $spacing-md;
  margin-bottom: $spacing-xl;

  .home-button {
    background: linear-gradient(135deg, var(--primary-color) 0%, var(--primary-light) 100%);
    border: none;
    padding: $spacing-md $spacing-lg;

    &:hover {
      background: linear-gradient(135deg, var(--primary-light) 0%, var(--primary-dark) 100%);
    }
  }

  .back-button {
    padding: $spacing-md $spacing-lg;
  }
}

.quick-nav {
  margin-top: $spacing-xl;
  padding-top: $spacing-xl;
  border-top: 1px solid var(--border-color);

  h3 {
    font-size: var(--font-size-lg);
    color: var(--text-primary);
    margin-bottom: $spacing-md;
    font-weight: 600;
  }

  .quick-links {
    display: flex;
    justify-content: center;
    gap: $spacing-lg;
    flex-wrap: wrap;

    .quick-link {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: $spacing-xs;
      padding: $spacing-md;
      border-radius: $border-radius-medium;
      background-color: var(--white);
      box-shadow: $shadow-light;
      text-decoration: none;
      color: var(--text-primary);
      font-size: var(--font-size-sm);
      transition: all 0.3s ease;
      min-width: 100px;

      .el-icon {
        font-size: 24px;
        color: var(--primary-color);
      }

      &:hover {
        transform: translateY(-2px);
        box-shadow: $shadow-medium;
        color: var(--primary-color);
      }
    }
  }
}

// 响应式设计
@include mobile {
  .not-found-content {
    padding: $spacing-lg;
  }

  .error-code {
    font-size: 6rem !important;
  }

  .error-title {
    font-size: var(--font-size-xl) !important;
  }

  .error-description {
    font-size: var(--font-size-md) !important;
  }

  .not-found-actions {
    flex-direction: column;
    align-items: center;

    .home-button,
    .back-button {
      width: 200px;
    }
  }

  .quick-links {
    flex-direction: column;
    gap: $spacing-md !important;

    .quick-link {
      flex-direction: row;
      justify-content: flex-start;
      text-align: left;
      min-width: auto;
      width: 100%;
    }
  }
}
</style>