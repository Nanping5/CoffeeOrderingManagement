"""订单数据模型"""
from datetime import datetime
from extensions import db
from sqlalchemy import func

class Order(db.Model):
    """订单模型"""
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    total_price = db.Column(db.Numeric(10, 2), nullable=False)
    status = db.Column(db.Enum('pending', 'preparing', 'ready', 'completed', 'cancelled'),
                       default='pending', nullable=False, index=True)
    customer_name = db.Column(db.String(100), nullable=True)
    customer_phone = db.Column(db.String(20), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    # 关系
    order_items = db.relationship('OrderItem', backref='order', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, user_id, order_number, total_price, customer_name=None, customer_phone=None, notes=None):
        """初始化订单"""
        self.user_id = user_id
        self.order_number = order_number
        self.total_price = total_price
        self.customer_name = customer_name
        self.customer_phone = customer_phone
        self.notes = notes

    def to_dict(self, include_items=False):
        """转换为字典"""
        data = {
            'id': self.id,
            'user_id': self.user_id,
            'order_number': self.order_number,
            'total_price': float(self.total_price),
            'status': self.status,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
            'item_count': self.order_items.count()
        }

        if include_items:
            data['order_items'] = [item.to_dict() for item in self.order_items]

        return data

    @staticmethod
    def from_dict(data):
        """从字典创建订单"""
        return Order(
            user_id=data.get('user_id'),
            order_number=data.get('order_number'),
            total_price=data.get('total_price'),
            customer_name=data.get('customer_name'),
            customer_phone=data.get('customer_phone'),
            notes=data.get('notes')
        )

    def update_from_dict(self, data):
        """从字典更新订单"""
        for key, value in data.items():
            if hasattr(self, key) and key not in ['id', 'order_number', 'created_at', 'user_id', 'order_items']:
                setattr(self, key, value)

    def get_items(self):
        """获取订单项"""
        return self.order_items.all()

    def calculate_total(self):
        """重新计算订单总价"""
        total = db.session.query(func.sum(OrderItem.subtotal)).filter_by(order_id=self.id).scalar()
        self.total_price = total if total else 0
        return self.total_price

    def add_item(self, menu_id, quantity, unit_price):
        """添加订单项"""
        subtotal = unit_price * quantity
        order_item = OrderItem(
            order_id=self.id,
            menu_id=menu_id,
            quantity=quantity,
            unit_price=unit_price,
            subtotal=subtotal
        )
        db.session.add(order_item)
        self.calculate_total()
        return order_item

    def update_status(self, status):
        """更新订单状态"""
        valid_statuses = ['pending', 'preparing', 'ready', 'completed', 'cancelled']
        if status in valid_statuses:
            self.status = status
            return True
        return False

    def can_cancel(self):
        """检查订单是否可以取消"""
        return self.status in ['pending', 'preparing']

    def cancel(self):
        """取消订单"""
        if self.can_cancel():
            self.status = 'cancelled'
            return True
        return False

    @staticmethod
    def generate_order_number():
        """生成订单号"""
        from datetime import datetime
        date_prefix = datetime.now().strftime('%Y%m%d')

        # 查找当天最大的订单号
        last_order = Order.query.filter(
            Order.order_number.like(f'CO{date_prefix}%')
        ).order_by(Order.order_number.desc()).first()

        if last_order:
            last_number = int(last_order.order_number[-4:])
            new_number = last_number + 1
        else:
            new_number = 1

        return f'CO{date_prefix}{new_number:04d}'

    @staticmethod
    def get_by_status(status):
        """按状态获取订单"""
        return Order.query.filter_by(status=status).all()

    @staticmethod
    def get_by_date_range(start_date, end_date):
        """按日期范围获取订单"""
        return Order.query.filter(
            Order.created_at >= start_date,
            Order.created_at <= end_date
        ).all()

    @staticmethod
    def get_revenue_by_date_range(start_date, end_date):
        """获取指定日期范围内的总收入"""
        total = db.session.query(func.sum(Order.total_price)).filter(
            Order.status.in_(['completed', 'ready']),
            Order.created_at >= start_date,
            Order.created_at <= end_date
        ).scalar()
        return float(total) if total else 0.0

    def __repr__(self):
        return f'<Order {self.order_number}>'