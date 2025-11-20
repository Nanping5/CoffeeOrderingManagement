"""数据模型包"""
from .user import User
from .menu import MenuItem
from .order import Order
from .order_item import OrderItem

# 导入所有模型，确保它们在SQLAlchemy中注册
__all__ = ['User', 'MenuItem', 'Order', 'OrderItem']