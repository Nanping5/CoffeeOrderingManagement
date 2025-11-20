"""订单项数据模型"""
from datetime import datetime
from extensions import db

class OrderItem(db.Model):
    """订单项模型"""
    __tablename__ = 'order_items'

    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    menu_id = db.Column(db.Integer, db.ForeignKey('menu_items.id'), nullable=False, index=True)
    quantity = db.Column(db.Integer, nullable=False)
    unit_price = db.Column(db.Numeric(10, 2), nullable=False)
    subtotal = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, order_id, menu_id, quantity, unit_price):
        """初始化订单项"""
        self.order_id = order_id
        self.menu_id = menu_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.subtotal = quantity * unit_price

    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'menu_id': self.menu_id,
            'menu_item': {
                'id': self.menu_item.id,
                'name': self.menu_item.name,
                'price': float(self.menu_item.price),
                'image_url': self.menu_item.image_url
            } if self.menu_item else None,
            'quantity': self.quantity,
            'unit_price': float(self.unit_price),
            'subtotal': float(self.subtotal),
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

    @staticmethod
    def from_dict(data):
        """从字典创建订单项"""
        order_item = OrderItem(
            order_id=data.get('order_id'),
            menu_id=data.get('menu_id'),
            quantity=data.get('quantity'),
            unit_price=data.get('unit_price')
        )
        return order_item

    def update_from_dict(self, data):
        """从字典更新订单项"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'order_id', 'created_at']:
                setattr(self, key, value)

        # 重新计算小计
        self.subtotal = self.quantity * self.unit_price
        return self

    def update_quantity(self, quantity):
        """更新数量"""
        if quantity > 0:
            self.quantity = quantity
            self.subtotal = quantity * self.unit_price
            return True
        return False

    def get_total_price(self):
        """获取总价"""
        return self.quantity * self.unit_price

    @staticmethod
    def get_by_order(order_id):
        """根据订单ID获取订单项"""
        return OrderItem.query.filter_by(order_id=order_id).all()

    @staticmethod
    def get_by_menu_item(menu_id):
        """根据菜单项ID获取所有订单项"""
        return OrderItem.query.filter_by(menu_id=menu_id).all()

    @staticmethod
    def get_popular_items(limit=10):
        """获取热门商品（按销量排序）"""
        from sqlalchemy import func
        return db.session.query(
            OrderItem.menu_id,
            func.sum(OrderItem.quantity).label('total_quantity')
        ).group_by(OrderItem.menu_id).order_by(
            func.sum(OrderItem.quantity).desc()
        ).limit(limit).all()

    def __repr__(self):
        return f'<OrderItem {self.order_id}-{self.menu_id}>'