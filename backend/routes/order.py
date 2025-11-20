"""订单路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.order_service import OrderService
from utils.auth_utils import token_required, admin_required, get_current_user, get_current_user_id

order_bp = Blueprint('order', __name__)

@order_bp.route('/', methods=['POST'])
@token_required
def create_order():
    """创建订单"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'errors': ['请提供订单信息']}), 400

        current_user_id = get_jwt_identity()
        result = OrderService.create_order(current_user_id, data)

        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/', methods=['GET'])
@token_required
def get_orders():
    """获取订单列表"""
    try:
        current_user = get_current_user()
        current_user_id = get_jwt_identity()

        # 获取查询参数
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # 管理员查看所有订单，普通用户只看自己的订单
        if current_user.is_admin():
            result = OrderService.get_all_orders(status, page, per_page)
        else:
            result = OrderService.get_user_orders(current_user_id, status, page, per_page)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/<int:order_id>', methods=['GET'])
@token_required
def get_order(order_id):
    """获取订单详情"""
    try:
        current_user = get_current_user()
        current_user_id = get_jwt_identity()

        result = OrderService.get_order_by_id(
            order_id, current_user_id, current_user.is_admin()
        )

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/<int:order_id>/status', methods=['PUT'])
@admin_required
def update_order_status(order_id):
    """更新订单状态（仅管理员）"""
    try:
        data = request.get_json()
        if not data or 'status' not in data:
            return jsonify({'success': False, 'errors': ['请提供订单状态']}), 400

        new_status = data['status']
        valid_statuses = ['pending', 'preparing', 'ready', 'completed', 'cancelled']

        if new_status not in valid_statuses:
            return jsonify({'success': False, 'errors': ['无效的订单状态']}), 400

        result = OrderService.update_order_status(order_id, new_status, is_admin=True)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/<int:order_id>/cancel', methods=['PUT'])
@token_required
def cancel_order(order_id):
    """取消订单"""
    try:
        current_user = get_current_user()
        current_user_id = get_jwt_identity()

        result = OrderService.cancel_order(
            order_id, current_user_id, current_user.is_admin()
        )

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/my', methods=['GET'])
@token_required
def get_my_orders():
    """获取当前用户的订单"""
    try:
        current_user_id = get_jwt_identity()

        # 获取查询参数
        status = request.args.get('status')
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        result = OrderService.get_user_orders(current_user_id, status, page, per_page)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/statistics', methods=['GET'])
@admin_required
def get_order_statistics():
    """获取订单统计信息（仅管理员）"""
    try:
        # 获取查询参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # 转换日期格式
        from datetime import datetime
        if start_date:
            start_date = datetime.fromisoformat(start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)

        result = OrderService.get_order_statistics(start_date, end_date)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/sales/daily', methods=['GET'])
@admin_required
def get_daily_sales():
    """获取每日销售数据（仅管理员）"""
    try:
        # 获取查询参数
        start_date = request.args.get('start_date')
        end_date = request.args.get('end_date')

        # 转换日期格式
        from datetime import datetime
        if start_date:
            start_date = datetime.fromisoformat(start_date)
        if end_date:
            end_date = datetime.fromisoformat(end_date)

        result = OrderService.get_daily_sales(start_date, end_date)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/count', methods=['GET'])
@admin_required
def get_order_count():
    """获取订单总数（仅管理员）"""
    try:
        from models.order import Order
        from extensions import db

        # 总订单数
        total_orders = Order.query.count()

        # 待处理订单数
        pending_orders = Order.query.filter_by(status='pending').count()

        # 准备中订单数
        preparing_orders = Order.query.filter_by(status='preparing').count()

        # 今日订单数
        from datetime import date
        today = date.today()
        today_orders = Order.query.filter(
            db.func.date(Order.created_at) == today
        ).count()

        return jsonify({
            'success': True,
            'counts': {
                'total_orders': total_orders,
                'pending_orders': pending_orders,
                'preparing_orders': preparing_orders,
                'today_orders': today_orders
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/recent', methods=['GET'])
@admin_required
def get_recent_orders():
    """获取最近订单（仅管理员）"""
    try:
        limit = int(request.args.get('limit', 10))

        recent_orders = Order.query.order_by(
            Order.created_at.desc()
        ).limit(limit).all()

        orders = []
        for order in recent_orders:
            order_data = order.to_dict(include_items=True)
            order_data['user'] = {
                'id': order.user.id,
                'username': order.user.username
            }
            orders.append(order_data)

        return jsonify({
            'success': True,
            'orders': orders
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/status/<status>', methods=['GET'])
@token_required
def get_orders_by_status(status):
    """根据状态获取订单"""
    try:
        current_user = get_current_user()
        current_user_id = get_jwt_identity()

        # 验证状态
        valid_statuses = ['pending', 'preparing', 'ready', 'completed', 'cancelled']
        if status not in valid_statuses:
            return jsonify({'success': False, 'errors': ['无效的订单状态']}), 400

        # 获取分页参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        if current_user.is_admin():
            result = OrderService.get_all_orders(status, page, per_page)
        else:
            result = OrderService.get_user_orders(current_user_id, status, page, per_page)

        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@order_bp.route('/search', methods=['GET'])
@admin_required
def search_orders():
    """搜索订单（仅管理员）"""
    try:
        keyword = request.args.get('q', '').strip()
        if not keyword:
            return jsonify({'success': False, 'errors': ['搜索关键词不能为空']}), 400

        # 获取分页参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 10))

        # 搜索订单号或用户名
        from models.order import Order
        from models.user import User
        from extensions import db

        query = Order.query.join(User).filter(
            db.or_(
                Order.order_number.like(f'%{keyword}%'),
                User.username.like(f'%{keyword}%'),
                User.email.like(f'%{keyword}%')
            )
        ).order_by(Order.created_at.desc())

        # 分页
        pagination = query.paginate(page=page, per_page=per_page, error_out=False)

        orders = []
        for order in pagination.items:
            order_data = order.to_dict(include_items=True)
            order_data['user'] = {
                'id': order.user.id,
                'username': order.user.username,
                'email': order.user.email
            }
            orders.append(order_data)

        return jsonify({
            'success': True,
            'orders': orders,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages,
            'keyword': keyword
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500