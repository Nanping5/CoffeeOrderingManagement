"""认证路由"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_refresh_token
from services.auth_service import AuthService
from utils.auth_utils import token_required

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """用户注册"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'errors': ['请提供注册信息']}), 400

        result = AuthService.register_user(data)
        if result['success']:
            return jsonify(result), 201
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """用户登录"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'errors': ['请提供登录信息']}), 400

        result = AuthService.login_user(data)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'服务器错误: {str(e)}']}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """刷新Token"""
    try:
        current_user_id = get_jwt_identity()
        result = AuthService.refresh_token(current_user_id)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 401

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'Token刷新失败: {str(e)}']}), 500

@auth_bp.route('/profile', methods=['GET'])
@token_required
def get_profile():
    """获取用户资料"""
    try:
        current_user_id = get_jwt_identity()
        result = AuthService.get_user_profile(current_user_id)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 404

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'获取用户信息失败: {str(e)}']}), 500

@auth_bp.route('/profile', methods=['PUT'])
@token_required
def update_profile():
    """更新用户资料"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'errors': ['请提供更新信息']}), 400

        result = AuthService.update_user_profile(current_user_id, data)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'更新失败: {str(e)}']}), 500

@auth_bp.route('/change-password', methods=['POST'])
@token_required
def change_password():
    """修改密码"""
    try:
        current_user_id = get_jwt_identity()
        data = request.get_json()
        if not data:
            return jsonify({'success': False, 'errors': ['请提供密码信息']}), 400

        result = AuthService.change_password(current_user_id, data)
        if result['success']:
            return jsonify(result), 200
        else:
            return jsonify(result), 400

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'密码修改失败: {str(e)}']}), 500

@auth_bp.route('/logout', methods=['POST'])
@token_required
def logout():
    """用户登出"""
    try:
        result = AuthService.logout_user()
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'success': False, 'errors': [f'登出失败: {str(e)}']}), 500

@auth_bp.route('/verify-token', methods=['GET'])
@token_required
def verify_token():
    """验证Token有效性"""
    try:
        current_user_id = get_jwt_identity()
        result = AuthService.get_user_profile(current_user_id)
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Token有效',
                'user': result['user']
            }), 200
        else:
            return jsonify({'success': False, 'message': 'Token无效'}), 401

    except Exception as e:
        return jsonify({'success': False, 'message': 'Token验证失败'}), 500

@auth_bp.route('/user-info', methods=['GET'])
@token_required
def get_user_info():
    """获取当前用户基本信息（用于前端权限判断）"""
    try:
        current_user_id = get_jwt_identity()
        from models.user import User
        user = User.query.get(current_user_id)

        if not user:
            return jsonify({'success': False, 'message': '用户不存在'}), 404

        return jsonify({
            'success': True,
            'user': {
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'role': user.role
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': '获取用户信息失败'}), 500