# 咖啡点餐管理系统

基于 **Flask + Vue3 + MySQL** 的现代化咖啡点餐管理系统，支持用户和管理员双角色，提供完整的点餐、购物车、订单管理等功能。

## 🚀 项目特性

### 🎨 用户体验
- **响应式设计** - 完美适配桌面端和移动端
- **现代化UI** - 基于 Element Plus + Animate.css 的美观界面
- **流畅动画** - 丰富的页面过渡和交互动画效果
- **直观操作** - 简洁明了的用户界面，易于使用

### 🛠️ 技术架构
- **前后端分离** - RESTful API 设计，前端 SPA 应用
- **模块化开发** - 清晰的代码结构，便于维护和扩展
- **状态管理** - Pinia 状态管理，数据流清晰
- **权限控制** - JWT 认证，用户/管理员角色分离

### 📱 核心功能
- **用户端功能**
  - 菜单浏览与搜索
  - 购物车管理
  - 订单创建与跟踪
  - 个人中心管理
  - 收藏商品功能

- **管理端功能** (开发中)
  - 菜单管理
  - 订单管理
  - 用户管理
  - 数据统计

## 🏗️ 技术栈

### 后端
- **框架**: Flask 2.3.3
- **数据库**: MySQL + SQLAlchemy ORM
- **认证**: Flask-JWT-Extended
- **验证**: Flask-Marshmallow + Marshmallow-SQLAlchemy
- **安全**: Flask-Bcrypt (密码加密)
- **跨域**: Flask-CORS
- **文件处理**: Pillow + Werkzeug

### 前端
- **框架**: Vue 3.3.4
- **构建工具**: Vite 4.4.9
- **UI组件**: Element Plus 2.3.9 + Animate.css 4.1.1
- **状态管理**: Pinia 2.1.6
- **路由**: Vue Router 4.2.4
- **HTTP客户端**: Axios 1.5.0
- **样式**: SCSS + Tailwind CSS

## 📁 项目结构

```
Demo/
├── backend/              # Flask 后端
│   ├── app.py           # 主应用入口
│   ├── config.py        # 配置管理
│   ├── models/          # 数据模型
│   │   ├── user.py      # 用户模型
│   │   ├── menu.py      # 菜单模型
│   │   ├── order.py     # 订单模型
│   │   └── order_item.py # 订单明细模型
│   ├── routes/          # API 路由
│   │   ├── auth.py      # 认证路由
│   │   ├── menu.py      # 菜单路由
│   │   ├── order.py     # 订单路由
│   │   └── user.py      # 用户路由
│   ├── services/        # 业务逻辑层
│   └── utils/           # 工具函数
├── frontend/            # Vue3 前端
│   ├── src/
│   │   ├── components/  # 公共组件
│   │   │   ├── AppHeader.vue      # 应用头部
│   │   │   ├── AppFooter.vue      # 应用底部
│   │   │   ├── CoffeeCard.vue     # 咖啡卡片
│   │   │   └── CartFloatButton.vue # 购物车浮动按钮
│   │   ├── views/         # 页面组件
│   │   │   ├── MenuPage.vue      # 菜单浏览
│   │   │   ├── CartPage.vue      # 购物车
│   │   │   ├── OrderPage.vue     # 订单管理
│   │   │   ├── ProfilePage.vue   # 个人中心
│   │   │   ├── LoginPage.vue     # 登录页面
│   │   │   └── RegisterPage.vue  # 注册页面
│   │   ├── api/           # API 封装
│   │   ├── store/         # Pinia 状态管理
│   │   ├── router/        # 路由配置
│   │   ├── utils/         # 工具函数
│   │   ├── composables/   # 组合式函数
│   │   └── layouts/       # 布局组件
├── database/             # 数据库脚本
│   ├── schema.sql        # 表结构
│   └── init_data.sql     # 初始数据
└── 项目进度报告.md       # 开发进度
```

## 🚀 快速开始

### 环境要求
- Python 3.8+
- Node.js 16+
- MySQL 8.0+

### 后端启动
```bash
# 进入后端目录
cd backend

# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或
.venv\Scripts\activate     # Windows

# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件，配置数据库连接等信息

# 初始化数据库
python run.py init-db

# 启动应用
python run.py
```

### 前端启动
```bash
# 进入前端目录
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev

# 构建生产版本
npm run build
```

### 数据库配置
```sql
-- 创建数据库
CREATE DATABASE coffee_ordering DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- 创建用户 (可选)
CREATE USER 'coffee_user'@'localhost' IDENTIFIED BY 'your_password';
GRANT ALL PRIVILEGES ON coffee_ordering.* TO 'coffee_user'@'localhost';
FLUSH PRIVILEGES;
```

## 🎯 功能特性

### 📱 用户功能
- **菜单浏览** - 商品展示、分类筛选、搜索功能
- **购物车** - 添加/删除商品、数量调整、价格计算
- **订单管理** - 创建订单、查看订单历史、订单状态跟踪
- **个人中心** - 用户信息管理、地址管理、订单统计
- **收藏功能** - 收藏喜欢的商品

### 🎨 UI/UX 设计
- **响应式布局** - 完美适配各种屏幕尺寸
- **现代化设计** - 简洁美观的界面设计
- **动画效果** - 丰富的页面过渡和交互动画
- **用户体验** - 直观的操作流程，友好的错误提示

### 🔒 安全特性
- **JWT 认证** - 安全的用户身份验证
- **密码加密** - Bcrypt 加密存储用户密码
- **权限控制** - 基于角色的访问控制
- **输入验证** - 前后端双重数据验证
- **SQL 注入防护** - ORM 防护 + 参数化查询

## 📊 项目进度

- ✅ **后端开发** - Flask 应用、API 接口、数据模型 (100%)
- ✅ **前端基础** - Vue3 应用、路由、状态管理 (100%)
- ✅ **用户界面** - 菜单、购物车、订单、个人中心 (100%)
- ✅ **公共组件** - 头部、底部、卡片组件 (90%)
- ✅ **动画效果** - Animate.css 集成、页面过渡 (100%)
- 🚧 **管理后台** - 管理员功能开发中 (0%)
- 📋 **测试优化** - 单元测试、性能优化 (0%)

**总体完成度: 75%**

## 🔄 核心业务流程

### 用户点餐流程
1. **浏览菜单** - 用户浏览咖啡菜单，可按分类筛选或搜索
2. **加入购物车** - 选择商品，添加到购物车，调整数量
3. **查看购物车** - 确认商品，使用优惠券，查看费用明细
4. **创建订单** - 填写配送信息，选择支付方式，提交订单
5. **订单跟踪** - 查看订单状态，等待配送完成
6. **评价订单** - 对订单进行评价和反馈

### 管理员流程 (开发中)
1. **菜单管理** - 添加、编辑、删除菜单项
2. **订单管理** - 查看、处理、更新订单状态
3. **用户管理** - 用户信息管理、权限控制
4. **数据统计** - 销售统计、用户分析、报表生成

## 🎨 设计规范

### 色彩系统
- **主色调**: #8b4513 (咖啡棕)
- **辅助色**: #f39c12 (金黄色)
- **成功色**: #27ae60 (绿色)
- **警告色**: #f39c12 (橙色)
- **危险色**: #e74c3c (红色)

### 组件规范
- **按钮**: 圆角设计，悬停动画效果
- **卡片**: 阴影效果，悬停提升
- **表单**: 统一的输入框样式，验证提示
- **导航**: 响应式菜单，图标配合文字

### 动画规范
- **页面切换**: 滑动、淡入淡出过渡
- **列表项**: 交错进入动画
- **按钮点击**: 反馈动画效果
- **加载状态**: 脉冲、旋转动画

## 🤝 贡献指南

1. Fork 项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📝 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情

## 🙏 致谢

- [Vue.js](https://vuejs.org/) - 渐进式 JavaScript 框架
- [Flask](https://flask.palletsprojects.com/) - Python Web 框架
- [Element Plus](https://element-plus.org/) - Vue 3 UI 组件库
- [Animate.css](https://animate.style/) - CSS 动画库
- [MySQL](https://www.mysql.com/) - 关系型数据库

---

**开发团队**: 咖啡点餐系统开发小组
**最后更新**: 2024年11月20日
**版本**: v1.0.0-beta