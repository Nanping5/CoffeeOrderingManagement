"""订单服务"""
from models.order import Order
from models.order_item import OrderItem
from models.menu import MenuItem
from models.user import User
from extensions import db
from datetime import datetime, timedelta
from sqlalchemy import func

class OrderService:
    """订单服务类"""

    @staticmethod
    def create_order(user_id, order_data):
        """创建订单"""
        try:
            # 验证订单数据
            errors = OrderService._validate_order_data(order_data)
            if errors:
                return {'success': False, 'errors': errors}

            # 验证商品并计算总价
            cart_items = order_data.get('items', [])
            if not cart_items:
                return {'success': False, 'errors': ['购物车为空']}

            total_price = 0
            validated_items = []

            for item in cart_items:
                menu_item = MenuItem.query.get(item['menu_id'])
                if not menu_item:
                    return {'success': False, 'errors': [f"商品ID {item['menu_id']} 不存在"]}

                if not menu_item.is_available:
                    return {'success': False, 'errors': [f"商品 {menu_item.name} 已下架"]}

                quantity = item.get('quantity', 1)
                if quantity <= 0:
                    return {'success': False, 'errors': [f"商品 {menu_item.name} 数量无效"]}

                subtotal = menu_item.price * quantity
                total_price += subtotal

                validated_items.append({
                    'menu_id': menu_item.id,
                    'quantity': quantity,
                    'unit_price': menu_item.price,
                    'subtotal': subtotal
                })

            # 生成订单号
            order_number = Order.generate_order_number()

            # 创建订单
            order = Order(
                user_id=user_id,
                order_number=order_number,
                total_price=total_price,
                customer_name=order_data.get('customer_name'),
                customer_phone=order_data.get('customer_phone'),
                notes=order_data.get('notes')
            )

            db.session.add(order)
            db.session.flush()  # 获取order.id

            # 创建订单项
            for item_data in validated_items:
                order_item = OrderItem(
                    order_id=order.id,
                    menu_id=item_data['menu_id'],
                    quantity=item_data['quantity'],
                    unit_price=item_data['unit_price'],
                    subtotal=item_data['subtotal']
                )
                db.session.add(order_item)

            db.session.commit()

            return {
                'success': True,
                'message': '订单创建成功',
                'order': order.to_dict(include_items=True)
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'创建订单失败: {str(e)}']}

    @staticmethod
    def get_user_orders(user_id, status=None, page=1, per_page=10):
        """获取用户订单列表"""
        try:
            query = Order.query.filter_by(user_id=user_id)

            # 状态筛选
            if status:
                query = query.filter_by(status=status)

            # 按创建时间倒序
            query = query.order_by(Order.created_at.desc())

            # 分页
            pagination = query.paginate(
                page=page, per_page=per_page, error_out=False
            )

            orders = []
            for order in pagination.items:
                order_data = order.to_dict(include_items=True)
                orders.append(order_data)

            return {
                'success': True,
                'orders': orders,
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取订单失败: {str(e)}']}

    @staticmethod
    def get_all_orders(status=None, page=1, per_page=10):
        """获取所有订单（管理员用）"""
        try:
            query = Order.query

            # 状态筛选
            if status:
                query = query.filter_by(status=status)

            # 按创建时间倒序
            query = query.order_by(Order.created_at.desc())

            # 分页
            pagination = query.paginate(
                page=page, per_page=per_page, error_out=False
            )

            orders = []
            for order in pagination.items:
                order_data = order.to_dict(include_items=True)
                # 添加用户信息
                order_data['user'] = {
                    'id': order.user.id,
                    'username': order.user.username,
                    'email': order.user.email
                }
                orders.append(order_data)

            return {
                'success': True,
                'orders': orders,
                'total': pagination.total,
                'page': page,
                'per_page': per_page,
                'pages': pagination.pages
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取订单失败: {str(e)}']}

    @staticmethod
    def get_order_by_id(order_id, user_id=None, is_admin=False):
        """获取订单详情"""
        try:
            order = Order.query.get(order_id)
            if not order:
                return {'success': False, 'errors': ['订单不存在']}

            # 权限检查
            if not is_admin and order.user_id != user_id:
                return {'success': False, 'errors': ['无权限查看此订单']}

            order_data = order.to_dict(include_items=True)

            # 添加用户信息（管理员用）
            if is_admin:
                order_data['user'] = {
                    'id': order.user.id,
                    'username': order.user.username,
                    'email': order.user.email,
                    'phone': order.user.phone
                }

            return {
                'success': True,
                'order': order_data
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取订单详情失败: {str(e)}']}

    @staticmethod
    def update_order_status(order_id, status, is_admin=False):
        """更新订单状态"""
        try:
            order = Order.query.get(order_id)
            if not order:
                return {'success': False, 'errors': ['订单不存在']}

            # 验证状态流转
            valid_transitions = {
                'pending': ['preparing', 'cancelled'],
                'preparing': ['ready', 'cancelled'],
                'ready': ['completed'],
                'completed': [],  # 已完成订单不能再修改状态
                'cancelled': []   # 已取消订单不能再修改状态
            }

            current_status = order.status
            if status not in valid_transitions.get(current_status, []):
                return {'success': False, 'errors': [f'不能从 {current_status} 状态变更为 {status}']}

            # 更新状态
            order.update_status(status)
            db.session.commit()

            return {
                'success': True,
                'message': f'订单状态更新为 {status}',
                'order': order.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'更新订单状态失败: {str(e)}']}

    @staticmethod
    def cancel_order(order_id, user_id=None, is_admin=False):
        """取消订单"""
        try:
            order = Order.query.get(order_id)
            if not order:
                return {'success': False, 'errors': ['订单不存在']}

            # 权限检查
            if not is_admin and order.user_id != user_id:
                return {'success': False, 'errors': ['无权限取消此订单']}

            # 检查是否可以取消
            if not order.can_cancel():
                return {'success': False, 'errors': ['订单状态不允许取消']}

            # 取消订单
            if order.cancel():
                db.session.commit()
                return {
                    'success': True,
                    'message': '订单已取消',
                    'order': order.to_dict()
                }
            else:
                return {'success': False, 'errors': ['取消订单失败']}

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'取消订单失败: {str(e)}']}

    @staticmethod
    def get_order_statistics(start_date=None, end_date=None):
        """获取订单统计信息"""
        try:
            # 默认查询最近30天
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=30)

            query = Order.query.filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date
            )

            # 总订单数
            total_orders = query.count()

            # 按状态统计
            status_stats = db.session.query(
                Order.status,
                db.func.count(Order.id).label('count')
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date
            ).group_by(Order.status).all()

            status_summary = {}
            for status, count in status_stats:
                status_summary[status] = count

            # 总收入（已完成和已准备的订单）
            total_revenue = db.session.query(
                db.func.sum(Order.total_price)
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_(['completed', 'ready'])
            ).scalar() or 0

            # 平均订单金额
            avg_order_value = db.session.query(
                db.func.avg(Order.total_price)
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date
            ).scalar() or 0

            return {
                'success': True,
                'statistics': {
                    'period': {
                        'start_date': start_date.isoformat(),
                        'end_date': end_date.isoformat()
                    },
                    'total_orders': total_orders,
                    'total_revenue': float(total_revenue),
                    'avg_order_value': float(avg_order_value),
                    'status_breakdown': status_summary
                }
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取统计信息失败: {str(e)}']}

    @staticmethod
    def get_daily_sales(start_date=None, end_date=None):
        """获取每日销售数据"""
        try:
            if not end_date:
                end_date = datetime.utcnow()
            if not start_date:
                start_date = end_date - timedelta(days=7)

            daily_data = db.session.query(
                db.func.date(Order.created_at).label('date'),
                db.func.count(Order.id).label('order_count'),
                db.func.sum(Order.total_price).label('revenue')
            ).filter(
                Order.created_at >= start_date,
                Order.created_at <= end_date,
                Order.status.in_(['completed', 'ready'])
            ).group_by(
                db.func.date(Order.created_at)
            ).order_by('date').all()

            sales_data = []
            for date, order_count, revenue in daily_data:
                sales_data.append({
                    'date': date.isoformat(),
                    'order_count': order_count,
                    'revenue': float(revenue) if revenue else 0
                })

            return {
                'success': True,
                'daily_sales': sales_data
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取销售数据失败: {str(e)}']}

    @staticmethod
    def _validate_order_data(data):
        """验证订单数据"""
        errors = []

        if not data:
            errors.append('请提供订单信息')
            return errors

        # 验证订单项
        items = data.get('items', [])
        if not items:
            errors.append('购物车不能为空')
        else:
            for i, item in enumerate(items):
                if not isinstance(item, dict):
                    errors.append(f'订单项 {i+1} 格式错误')
                    continue

                if 'menu_id' not in item:
                    errors.append(f'订单项 {i+1} 缺少商品ID')
                if 'quantity' not in item:
                    errors.append(f'订单项 {i+1} 缺少数量')
                elif not isinstance(item['quantity'], int) or item['quantity'] <= 0:
                    errors.append(f'订单项 {i+1} 数量无效')

        # 验证客户信息（可选）
        customer_name = data.get('customer_name', '').strip()
        if customer_name and len(customer_name) > 100:
            errors.append('客户姓名不能超过100个字符')

        customer_phone = data.get('customer_phone', '').strip()
        if customer_phone:
            import re
            if not re.match(r'^1[3-9]\d{9}$', customer_phone):
                errors.append('手机号格式不正确')

        # 验证备注
        notes = data.get('notes', '').strip()
        if notes and len(notes) > 500:
            errors.append('备注不能超过500个字符')

        return errors