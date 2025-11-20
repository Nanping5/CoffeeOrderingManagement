"""菜单数据模型"""
from datetime import datetime
from extensions import db

class MenuItem(db.Model):
    """菜单项模型"""
    __tablename__ = 'menu'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    category = db.Column(db.String(50), nullable=False, default='coffee', index=True)
    image_url = db.Column(db.String(255), nullable=True)
    is_available = db.Column(db.Boolean, default=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关系
    order_items = db.relationship('OrderItem', backref='menu_item', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, name, price, description=None, category='coffee', image_url=None, is_available=True):
        """初始化菜单项"""
        self.name = name
        self.price = price
        self.description = description
        self.category = category
        self.image_url = image_url
        self.is_available = is_available

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': float(self.price),
            'category': self.category,
            'image_url': self.image_url,
            'is_available': self.is_available,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    @staticmethod
    def from_dict(data):
        """从字典创建菜单项"""
        return MenuItem(
            name=data.get('name'),
            price=data.get('price'),
            description=data.get('description'),
            category=data.get('category', 'coffee'),
            image_url=data.get('image_url'),
            is_available=data.get('is_available', True)
        )

    def update_from_dict(self, data):
        """从字典更新菜单项"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'created_at', 'order_items']:
                setattr(self, key, value)

    def get_order_count(self):
        """获取该菜单项被下单的次数"""
        return self.order_items.count()

    def get_total_quantity_sold(self):
        """获取该菜单项总销售数量"""
        from sqlalchemy import func
        total = db.session.query(func.sum(OrderItem.quantity)).filter_by(menu_id=self.id).scalar()
        return int(total) if total else 0

    def get_total_revenue(self):
        """获取该菜单项总收入"""
        from sqlalchemy import func
        total = db.session.query(func.sum(OrderItem.subtotal)).filter_by(menu_id=self.id).scalar()
        return float(total) if total else 0.0

    @staticmethod
    def get_by_category(category):
        """按分类获取菜单项"""
        return MenuItem.query.filter_by(category=category, is_available=True).all()

    @staticmethod
    def get_available():
        """获取可用的菜单项"""
        return MenuItem.query.filter_by(is_available=True).all()

    @staticmethod
    def get_categories():
        """获取所有分类"""
        categories = db.session.query(MenuItem.category).distinct().all()
        return [cat[0] for cat in categories]

    def __repr__(self):
        return f'<MenuItem {self.name}>'