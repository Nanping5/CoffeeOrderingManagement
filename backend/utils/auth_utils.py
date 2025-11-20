"""认证工具函数"""
from functools import wraps
from flask import jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity, get_jwt
from models.user import User

def token_required(f):
    """Token验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': 'Token验证失败', 'error': str(e)}), 401
    return decorated_function

def admin_required(f):
    """管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)

            if not current_user or current_user.role != 'admin':
                return jsonify({'message': '需要管理员权限'}), 403

            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': '权限验证失败', 'error': str(e)}), 401
    return decorated_function

def get_current_user():
    """获取当前登录用户"""
    try:
        verify_jwt_in_request()
        current_user_id = get_jwt_identity()
        return User.query.get(current_user_id)
    except:
        return None

def get_current_user_id():
    """获取当前登录用户ID"""
    try:
        verify_jwt_in_request()
        return get_jwt_identity()
    except:
        return None

def user_or_admin_required(f):
    """用户本人或管理员权限验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)

            if not current_user:
                return jsonify({'message': '用户不存在'}), 401

            # 检查是否为管理员或操作自己的资源
            user_id = kwargs.get('user_id')
            if current_user.role != 'admin' and user_id and str(current_user_id) != str(user_id):
                return jsonify({'message': '只能操作自己的资源'}), 403

            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'message': '权限验证失败', 'error': str(e)}), 401
    return decorated_function

def validate_registration_data(data):
    """验证注册数据"""
    errors = []

    if not data:
        errors.append('请提供注册信息')
        return errors

    if not data.get('username'):
        errors.append('用户名不能为空')
    elif len(data.get('username', '')) < 3:
        errors.append('用户名至少3个字符')
    elif len(data.get('username', '')) > 50:
        errors.append('用户名不能超过50个字符')

    if not data.get('email'):
        errors.append('邮箱不能为空')

    if not data.get('password'):
        errors.append('密码不能为空')
    elif len(data.get('password', '')) < 6:
        errors.append('密码至少6个字符')

    # 检查邮箱格式
    import re
    email = data.get('email', '')
    email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if email and not re.match(email_pattern, email):
        errors.append('邮箱格式不正确')

    return errors

def validate_login_data(data):
    """验证登录数据"""
    errors = []

    if not data:
        errors.append('请提供登录信息')
        return errors

    if not data.get('username') and not data.get('email'):
        errors.append('请提供用户名或邮箱')

    if not data.get('password'):
        errors.append('密码不能为空')

    return errors

def user_exists(username=None, email=None):
    """检查用户是否存在"""
    if username:
        user = User.query.filter_by(username=username).first()
        if user:
            return True

    if email:
        user = User.query.filter_by(email=email).first()
        if user:
            return True

    return False

import os
from werkzeug.utils import secure_filename

def allowed_file(filename, allowed_extensions=None):
    """检查文件扩展名是否允许"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, upload_folder='uploads', allowed_extensions=None):
    """保存上传的文件"""
    if file and allowed_file(file.filename, allowed_extensions):
        # 确保上传目录存在
        if not os.path.exists(upload_folder):
            os.makedirs(upload_folder)

        # 获取安全的文件名
        filename = secure_filename(file.filename)

        # 添加时间戳避免文件名冲突
        import time
        timestamp = str(int(time.time()))
        filename = f"{timestamp}_{filename}"

        # 保存文件
        file_path = os.path.join(upload_folder, filename)
        file.save(file_path)

        # 返回相对路径
        return f"/{upload_folder}/{filename}"

    return None