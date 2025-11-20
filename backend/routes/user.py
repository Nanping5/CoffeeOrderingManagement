"""用户管理路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.user import User
from extensions import db
from utils.auth_utils import admin_required, token_required

user_bp = Blueprint('user', __name__)

@user_bp.route('/', methods=['GET'])
@admin_required
def get_users():
    """获取所有用户列表（仅管理员）"""
    try:
        # 获取查询参数
        page = int(request.args.get('page', 1))
        per_page = int(request.args.get('per_page', 20))
        role = request.args.get('role')
        keyword = request.args.get('keyword', '').strip()

        query = User.query

        # 角色筛选
        if role:
            query = query.filter_by(role=role)

        # 关键词搜索
        if keyword:
            search_pattern = f'%{keyword}%'
            query = query.filter(
                db.or_(
                    User.username.like(search_pattern),
                    User.email.like(search_pattern)
                )
            )

        # 分页查询
        pagination = query.order_by(User.created_at.desc()).paginate(
            page=page, per_page=per_page, error_out=False
        )

        users = []
        for user in pagination.items:
            user_data = user.to_dict()
            # 添加额外统计信息
            user_data['order_count'] = user.get_order_count()
            user_data['total_spent'] = user.get_total_spent()
            users.append(user_data)

        return jsonify({
            'success': True,
            'users': users,
            'total': pagination.total,
            'page': page,
            'per_page': per_page,
            'pages': pagination.pages
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@user_bp.route('/<int:user_id>', methods=['GET'])
@admin_required
def get_user(user_id):
    """获取用户详情（仅管理员）"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'errors': ['用户不存在']}), 404

        user_data = user.to_dict()
        user_data['order_count'] = user.get_order_count()
        user_data['total_spent'] = user.get_total_spent()

        return jsonify({
            'success': True,
            'user': user_data
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@user_bp.route('/<int:user_id>', methods=['PUT'])
@admin_required
def update_user(user_id):
    """更新用户信息（仅管理员）"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'errors': ['用户不存在']}), 404

        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'errors': ['请提供更新信息']}), 400

        # 验证数据
        errors = []
        if 'email' in data:
            email = data.get('email', '').strip()
            if not email:
                errors.append('邮箱不能为空')
            else:
                # 检查邮箱格式
                import re
                if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    errors.append('邮箱格式不正确')
                # 检查邮箱是否已被使用
                elif email != user.email and User.query.filter_by(email=email).first():
                    errors.append('邮箱已被使用')

        if 'username' in data:
            username = data.get('username', '').strip()
            if not username or len(username) < 3:
                errors.append('用户名至少3个字符')
            elif username != user.username and User.query.filter_by(username=username).first():
                errors.append('用户名已被使用')

        if 'role' in data:
            role = data.get('role')
            if role not in ['admin', 'user']:
                errors.append('角色必须是 admin 或 user')

        if 'phone' in data:
            phone = data.get('phone', '').strip()
            if phone:
                import re
                if not re.match(r'^1[3-9]\d{9}$', phone):
                    errors.append('手机号格式不正确')

        if errors:
            return jsonify({'success': False, 'errors': errors}), 400

        # 更新用户信息
        allowed_fields = ['username', 'email', 'phone', 'role']
        for field in allowed_fields:
            if field in data:
                setattr(user, field, data[field])

        db.session.commit()

        return jsonify({
            'success': True,
            'message': '用户信息更新成功',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'errors': [f'更新失败: {str(e)}']}), 500

@user_bp.route('/<int:user_id>', methods=['DELETE'])
@admin_required
def delete_user(user_id):
    """删除用户（仅管理员）"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'errors': ['用户不存在']}), 404

        # 检查是否有关联订单
        if user.orders.count() > 0:
            return jsonify({'success': False, 'errors': ['该用户有关联订单，无法删除']}), 400

        db.session.delete(user)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '用户删除成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'errors': [f'删除失败: {str(e)}']}), 500

@user_bp.route('/<int:user_id>/reset-password', methods=['POST'])
@admin_required
def reset_user_password(user_id):
    """重置用户密码（仅管理员）"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'errors': ['用户不存在']}), 404

        data = request.get_json()
        if not data or 'new_password' not in data:
            return jsonify({'success': False, 'errors': ['请提供新密码']}), 400

        new_password = data['new_password']
        if len(new_password) < 6:
            return jsonify({'success': False, 'errors': ['密码至少6个字符']}), 400

        user.set_password(new_password)
        db.session.commit()

        return jsonify({
            'success': True,
            'message': '密码重置成功'
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'errors': [f'重置密码失败: {str(e)}']}), 500

@user_bp.route('/statistics', methods=['GET'])
@admin_required
def get_user_statistics():
    """获取用户统计信息（仅管理员）"""
    try:
        # 总用户数
        total_users = User.query.count()

        # 按角色统计
        admin_count = User.query.filter_by(role='admin').count()
        user_count = User.query.filter_by(role='user').count()

        # 今日注册用户数
        from datetime import date
        today = date.today()
        today_users = User.query.filter(
            db.func.date(User.created_at) == today
        ).count()

        # 最近7天注册用户数
        from datetime import timedelta
        week_ago = today - timedelta(days=7)
        week_users = User.query.filter(
            db.func.date(User.created_at) >= week_ago
        ).count()

        # 活跃用户（有订单记录的用户）
        active_users = db.session.query(User.id).join(User.orders).distinct().count()

        return jsonify({
            'success': True,
            'statistics': {
                'total_users': total_users,
                'admin_users': admin_count,
                'regular_users': user_count,
                'today_new_users': today_users,
                'week_new_users': week_users,
                'active_users': active_users
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'获取统计信息失败: {str(e)}']}), 500

@user_bp.route('/<int:user_id>/toggle-status', methods=['PATCH'])
@admin_required
def toggle_user_status(user_id):
    """切换用户状态（禁用/启用）（仅管理员）"""
    try:
        # 这里可以扩展用户模型，添加is_active字段
        # 目前只是示例实现
        user = User.query.get(user_id)
        if not user:
            return jsonify({'success': False, 'errors': ['用户不存在']}), 404

        # 实际实现需要修改用户模型，添加status字段
        return jsonify({
            'success': True,
            'message': '用户状态切换成功',
            'user': user.to_dict()
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'状态切换失败: {str(e)}']}), 500