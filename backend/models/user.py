"""用户数据模型"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from extensions import db, bcrypt

class User(db.Model):
    """用户模型"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(100), unique=True, nullable=False, index=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('admin', 'user'), default='user', nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关系
    orders = db.relationship('Order', backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, username, email, password, role='user', phone=None):
        """初始化用户"""
        self.username = username
        self.email = email
        self.set_password(password)
        self.role = role
        self.phone = phone

    def set_password(self, password):
        """设置密码（加密存储）"""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password):
        """验证密码"""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self, include_sensitive=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'phone': self.phone,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }
        if include_sensitive:
            data['password'] = self.password
        return data

    @staticmethod
    def from_dict(data):
        """从字典创建用户"""
        return User(
            username=data.get('username'),
            email=data.get('email'),
            password=data.get('password'),
            role=data.get('role', 'user'),
            phone=data.get('phone')
        )

    def update_from_dict(self, data):
        """从字典更新用户信息"""
        for key, value in data.items():
            if key == 'password' and value:
                self.set_password(value)
            elif hasattr(self, key) and key not in ['id', 'created_at']:
                setattr(self, key, value)

    def is_admin(self):
        """检查是否为管理员"""
        return self.role == 'admin'

    def get_order_count(self):
        """获取用户订单数量"""
        return self.orders.count()

    def get_total_spent(self):
        """获取用户总消费金额"""
        from sqlalchemy import func
        total = db.session.query(func.sum(Order.total_price)).filter_by(user_id=self.id).scalar()
        return float(total) if total else 0.0

    def __repr__(self):
        return f'<User {self.username}>'