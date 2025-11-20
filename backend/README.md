# 咖啡点餐管理系统 - 后端

基于Flask的咖啡点餐管理系统后端API服务。

## 技术栈
- Flask - Web框架
- Flask-SQLAlchemy - ORM
- Flask-Migrate - 数据库迁移
- Flask-JWT-Extended - JWT认证
- Flask-CORS - 跨域支持
- Flask-Bcrypt - 密码加密
- PyMySQL - MySQL数据库驱动
- Marshmallow - 数据序列化

## 安装依赖
```bash
pip install -r requirements.txt
```

## 配置环境变量
复制 `.env.example` 为 `.env` 并配置相应的环境变量：
```bash
cp .env.example .env
```

## 数据库设置
1. 创建MySQL数据库
2. 导入数据库结构：
```sql
mysql -u root -p < ../database/schema.sql
mysql -u root -p < ../database/init_data.sql
```

## 运行应用
```bash
python run.py
```
或
```bash
flask run --host=0.0.0.0 --port=5000
```

## API接口

### 认证相关 `/api/auth`
- `POST /register` - 用户注册
- `POST /login` - 用户登录
- `POST /refresh` - 刷新Token

### 用户管理 `/api/users`
- `GET /` - 获取用户列表（管理员）
- `GET /<id>` - 获取用户详情
- `PUT /<id>` - 更新用户信息
- `DELETE /<id>` - 删除用户（管理员）

### 菜单管理 `/api/menu`
- `GET /` - 获取菜单列表
- `GET /<id>` - 获取菜单项详情
- `POST /` - 添加菜单项（管理员）
- `PUT /<id>` - 更新菜单项（管理员）
- `DELETE /<id>` - 删除菜单项（管理员）

### 订单管理 `/api/orders`
- `GET /` - 获取订单列表
- `GET /<id>` - 获取订单详情
- `POST /` - 创建订单
- `PUT /<id>` - 更新订单状态
- `DELETE /<id>` - 删除订单

## 目录结构
```
backend/
├── app.py              # Flask应用工厂
├── config.py           # 配置文件
├── extensions.py       # 扩展初始化
├── run.py             # 运行脚本
├── models/            # 数据模型
├── routes/            # API路由
├── services/          # 业务逻辑
├── utils/             # 工具函数
├── static/            # 静态文件
├── templates/         # 模板文件
├── requirements.txt   # 依赖包
└── .env.example      # 环境变量示例
```