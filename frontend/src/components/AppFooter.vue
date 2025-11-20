<template>
  <footer class="app-footer">
    <div class="footer-content">
      <div class="footer-container">
        <!-- 主要内容区域 -->
        <div class="footer-main">
          <div class="footer-section">
            <div class="footer-logo">
              <el-icon class="logo-icon"><Coffee /></el-icon>
              <span class="logo-text">咖啡时光</span>
            </div>
            <p class="footer-description">
              为您提供最优质的咖啡体验，每一杯都是用心调制的艺术品。
            </p>
            <div class="social-links">
              <el-button
                v-for="social in socialLinks"
                :key="social.name"
                type="text"
                :icon="social.icon"
                circle
                size="small"
                class="social-btn"
                @click="handleSocialClick(social)"
              />
            </div>
          </div>

          <div class="footer-section">
            <h4 class="section-title">快速链接</h4>
            <ul class="footer-links">
              <li>
                <router-link to="/menu" class="footer-link">
                  <el-icon><Coffee /></el-icon>
                  咖啡菜单
                </router-link>
              </li>
              <li>
                <router-link to="/orders" class="footer-link">
                  <el-icon><List /></el-icon>
                  我的订单
                </router-link>
              </li>
              <li>
                <router-link to="/profile" class="footer-link">
                  <el-icon><User /></el-icon>
                  个人中心
                </router-link>
              </li>
              <li>
                <router-link to="/about" class="footer-link">
                  <el-icon><InfoFilled /></el-icon>
                  关于我们
                </router-link>
              </li>
            </ul>
          </div>

          <div class="footer-section">
            <h4 class="section-title">客户服务</h4>
            <ul class="footer-links">
              <li>
                <a href="#" class="footer-link" @click="handleContact">
                  <el-icon><Service /></el-icon>
                  联系我们
                </a>
              </li>
              <li>
                <a href="#" class="footer-link" @click="handleFAQ">
                  <el-icon><QuestionFilled /></el-icon>
                  常见问题
                </a>
              </li>
              <li>
                <a href="#" class="footer-link" @click="handlePrivacy">
                  <el-icon><Lock /></el-icon>
                  隐私政策
                </a>
              </li>
              <li>
                <a href="#" class="footer-link" @click="handleTerms">
                  <el-icon><Document /></el-icon>
                  服务条款
                </a>
              </li>
            </ul>
          </div>

          <div class="footer-section">
            <h4 class="section-title">联系信息</h4>
            <div class="contact-info">
              <div class="contact-item">
                <el-icon class="contact-icon"><LocationInformation /></el-icon>
                <span>北京市朝阳区建国门外大街1号</span>
              </div>
              <div class="contact-item">
                <el-icon class="contact-icon"><Phone /></el-icon>
                <span>400-123-4567</span>
              </div>
              <div class="contact-item">
                <el-icon class="contact-icon"><Message /></el-icon>
                <span>service@coffeetime.com</span>
              </div>
              <div class="contact-item">
                <el-icon class="contact-icon"><Clock /></el-icon>
                <span>营业时间: 08:00 - 22:00</span>
              </div>
            </div>
          </div>
        </div>

        <!-- 订阅区域 -->
        <div class="footer-subscribe">
          <div class="subscribe-content">
            <h4 class="subscribe-title">订阅我们</h4>
            <p class="subscribe-description">获取最新优惠和咖啡资讯</p>
            <div class="subscribe-form">
              <el-input
                v-model="email"
                placeholder="请输入您的邮箱"
                clearable
                class="subscribe-input"
              >
                <template #append>
                  <el-button
                    type="primary"
                    :loading="subscribing"
                    @click="handleSubscribe"
                  >
                    订阅
                  </el-button>
                </template>
              </el-input>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 版权信息 -->
    <div class="footer-bottom">
      <div class="footer-container">
        <div class="bottom-content">
          <div class="copyright">
            <p>&copy; 2024 咖啡时光. 保留所有权利.</p>
          </div>
          <div class="payment-methods">
            <span class="payment-title">支付方式:</span>
            <div class="payment-icons">
              <el-icon class="payment-icon"><CreditCard /></el-icon>
              <el-icon class="payment-icon"><Wallet /></el-icon>
              <el-icon class="payment-icon"><Coin /></el-icon>
            </div>
          </div>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup>
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import {
  Coffee,
  List,
  User,
  InfoFilled,
  Service,
  QuestionFilled,
  Lock,
  Document,
  LocationInformation,
  Phone,
  Message,
  Clock,
  CreditCard,
  Wallet,
  Coin,
  Share,
  ChatDotRound,
  Promotion,
  Notification
} from '@element-plus/icons-vue'

// 响应式数据
const email = ref('')
const subscribing = ref(false)

// 社交媒体链接
const socialLinks = [
  { name: '微信', icon: ChatDotRound, color: '#07c160' },
  { name: '微博', icon: Share, color: '#ff8200' },
  { name: '抖音', icon: Promotion, color: '#fe2c55' },
  { name: '通知', icon: Notification, color: '#1890ff' }
]

// 方法
const handleSocialClick = (social) => {
  ElMessage.info(`即将打开${social.name}页面`)
}

const handleContact = () => {
  ElMessage.info('跳转到联系我们页面')
}

const handleFAQ = () => {
  ElMessage.info('跳转到常见问题页面')
}

const handlePrivacy = () => {
  ElMessage.info('查看隐私政策')
}

const handleTerms = () => {
  ElMessage.info('查看服务条款')
}

const handleSubscribe = async () => {
  if (!email.value.trim()) {
    ElMessage.warning('请输入邮箱地址')
    return
  }

  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email.value)) {
    ElMessage.warning('请输入有效的邮箱地址')
    return
  }

  subscribing.value = true

  try {
    // 模拟订阅请求
    await new Promise(resolve => setTimeout(resolve, 1000))

    ElMessage.success('订阅成功！感谢您的关注')
    email.value = ''
  } catch (error) {
    ElMessage.error('订阅失败，请稍后重试')
  } finally {
    subscribing.value = false
  }
}
</script>

<style lang="scss" scoped>
.app-footer {
  background: linear-gradient(135deg, #2c3e50 0%, #34495e 100%);
  color: white;
  margin-top: auto;

  .footer-content {
    padding: 60px 0 30px;
  }

  .footer-container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 20px;
  }

  .footer-main {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 40px;
    margin-bottom: 40px;

    .footer-section {
      .footer-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        margin-bottom: 20px;

        .logo-icon {
          font-size: 2rem;
          color: #f39c12;
        }

        .logo-text {
          font-size: 1.5rem;
          font-weight: bold;
          background: linear-gradient(135deg, #f39c12, #e67e22);
          -webkit-background-clip: text;
          -webkit-text-fill-color: transparent;
          background-clip: text;
        }
      }

      .footer-description {
        color: #bdc3c7;
        line-height: 1.6;
        margin-bottom: 20px;
      }

      .social-links {
        display: flex;
        gap: 12px;

        .social-btn {
          background: rgba(255, 255, 255, 0.1);
          border: 1px solid rgba(255, 255, 255, 0.2);
          color: white;
          transition: all 0.3s ease;

          &:hover {
            background: #f39c12;
            border-color: #f39c12;
            transform: translateY(-2px);
          }
        }
      }

      .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 20px;
        color: #f39c12;
      }

      .footer-links {
        list-style: none;
        padding: 0;
        margin: 0;

        li {
          margin-bottom: 12px;

          .footer-link {
            display: flex;
            align-items: center;
            gap: 8px;
            color: #bdc3c7;
            text-decoration: none;
            transition: all 0.3s ease;
            padding: 4px 0;

            &:hover {
              color: #f39c12;
              transform: translateX(5px);
            }

            .el-icon {
              font-size: 1rem;
            }
          }
        }
      }

      .contact-info {
        .contact-item {
          display: flex;
          align-items: center;
          gap: 12px;
          margin-bottom: 12px;
          color: #bdc3c7;

          .contact-icon {
            color: #f39c12;
            font-size: 1.1rem;
            flex-shrink: 0;
          }
        }
      }
    }
  }

  .footer-subscribe {
    background: rgba(0, 0, 0, 0.2);
    border-radius: 12px;
    padding: 30px;
    text-align: center;

    .subscribe-content {
      max-width: 500px;
      margin: 0 auto;

      .subscribe-title {
        font-size: 1.5rem;
        font-weight: bold;
        margin-bottom: 10px;
        color: #f39c12;
      }

      .subscribe-description {
        color: #bdc3c7;
        margin-bottom: 20px;
      }

      .subscribe-form {
        .subscribe-input {
          :deep(.el-input-group__append) {
            padding: 0;

            .el-button {
              border: none;
              border-radius: 0 8px 8px 0;
              background: linear-gradient(135deg, #f39c12, #e67e22);
              color: white;
              font-weight: 500;

              &:hover {
                background: linear-gradient(135deg, #e67e22, #f39c12);
              }
            }
          }
        }
      }
    }
  }

  .footer-bottom {
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    padding: 20px 0;

    .bottom-content {
      display: flex;
      justify-content: space-between;
      align-items: center;
      flex-wrap: wrap;
      gap: 20px;

      .copyright {
        p {
          margin: 0;
          color: #95a5a6;
          font-size: 0.9rem;
        }
      }

      .payment-methods {
        display: flex;
        align-items: center;
        gap: 12px;

        .payment-title {
          color: #95a5a6;
          font-size: 0.9rem;
        }

        .payment-icons {
          display: flex;
          gap: 8px;

          .payment-icon {
            font-size: 1.2rem;
            color: #95a5a6;
            transition: all 0.3s ease;

            &:hover {
              color: #f39c12;
              transform: translateY(-2px);
            }
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .app-footer {
    .footer-content {
      padding: 40px 0 20px;
    }

    .footer-container {
      padding: 0 16px;
    }

    .footer-main {
      grid-template-columns: 1fr;
      gap: 30px;

      .footer-section {
        .footer-logo {
          justify-content: center;

          .logo-text {
            font-size: 1.3rem;
          }
        }

        .footer-description {
          text-align: center;
        }

        .social-links {
          justify-content: center;
        }

        .section-title {
          text-align: center;
        }

        .footer-links {
          text-align: center;

          li {
            .footer-link {
              justify-content: center;
            }
          }
        }

        .contact-info {
          .contact-item {
            justify-content: center;
            text-align: center;
          }
        }
      }
    }

    .footer-subscribe {
      padding: 20px;

      .subscribe-content {
        .subscribe-title {
          font-size: 1.3rem;
        }
      }
    }

    .footer-bottom {
      .bottom-content {
        flex-direction: column;
        text-align: center;

        .payment-methods {
          flex-direction: column;
          gap: 8px;
        }
      }
    }
  }
}

@media (max-width: 480px) {
  .app-footer {
    .footer-main {
      .footer-section {
        .footer-logo {
          .logo-icon {
            font-size: 1.8rem;
          }
        }

        .social-links {
          .social-btn {
            width: 36px;
            height: 36px;
          }
        }
      }
    }

    .footer-subscribe {
      .subscribe-form {
        .subscribe-input {
          :deep(.el-input__inner) {
            font-size: 0.9rem;
          }
        }
      }
    }
  }
}
</style>