"""认证服务"""
from models.user import User
from extensions import db
from utils.auth_utils import validate_registration_data, validate_login_data, user_exists
from flask_jwt_extended import create_access_token, create_refresh_token
import re

class AuthService:
    """认证服务类"""

    @staticmethod
    def register_user(user_data):
        """用户注册"""
        # 验证数据
        errors = validate_registration_data(user_data)
        if errors:
            return {'success': False, 'errors': errors}

        username = user_data.get('username')
        email = user_data.get('email')
        password = user_data.get('password')
        phone = user_data.get('phone')

        # 检查用户是否已存在
        if user_exists(username=username):
            return {'success': False, 'errors': ['用户名已存在']}

        if user_exists(email=email):
            return {'success': False, 'errors': ['邮箱已存在']}

        try:
            # 创建新用户
            new_user = User(
                username=username,
                email=email,
                password=password,
                phone=phone,
                role='user'
            )

            db.session.add(new_user)
            db.session.commit()

            # 生成Token
            access_token = create_access_token(identity=new_user.id)
            refresh_token = create_refresh_token(identity=new_user.id)

            return {
                'success': True,
                'message': '注册成功',
                'user': new_user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'注册失败: {str(e)}']}

    @staticmethod
    def login_user(login_data):
        """用户登录"""
        # 验证数据
        errors = validate_login_data(login_data)
        if errors:
            return {'success': False, 'errors': errors}

        username_or_email = login_data.get('username') or login_data.get('email')
        password = login_data.get('password')

        try:
            # 查找用户（用户名或邮箱）
            user = None
            if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', username_or_email):
                user = User.query.filter_by(email=username_or_email).first()
            else:
                user = User.query.filter_by(username=username_or_email).first()

            if not user:
                return {'success': False, 'errors': ['用户不存在']}

            if not user.check_password(password):
                return {'success': False, 'errors': ['密码错误']}

            # 生成Token
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)

            return {
                'success': True,
                'message': '登录成功',
                'user': user.to_dict(),
                'access_token': access_token,
                'refresh_token': refresh_token
            }

        except Exception as e:
            return {'success': False, 'errors': [f'登录失败: {str(e)}']}

    @staticmethod
    def refresh_token(user_id):
        """刷新Token"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'errors': ['用户不存在']}

            access_token = create_access_token(identity=user.id)

            return {
                'success': True,
                'message': 'Token刷新成功',
                'access_token': access_token
            }

        except Exception as e:
            return {'success': False, 'errors': [f'Token刷新失败: {str(e)}']}

    @staticmethod
    def get_user_profile(user_id):
        """获取用户资料"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'errors': ['用户不存在']}

            # 添加额外信息
            user_data = user.to_dict()
            user_data['order_count'] = user.get_order_count()
            user_data['total_spent'] = user.get_total_spent()

            return {
                'success': True,
                'user': user_data
            }

        except Exception as e:
            return {'success': False, 'errors': [f'获取用户信息失败: {str(e)}']}

    @staticmethod
    def update_user_profile(user_id, profile_data):
        """更新用户资料"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'errors': ['用户不存在']}

            # 验证数据
            errors = []
            if 'email' in profile_data:
                email = profile_data.get('email')
                if not email:
                    errors.append('邮箱不能为空')
                elif not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
                    errors.append('邮箱格式不正确')
                elif email != user.email and user_exists(email=email):
                    errors.append('邮箱已被使用')

            if 'username' in profile_data:
                username = profile_data.get('username')
                if not username or len(username) < 3:
                    errors.append('用户名至少3个字符')
                elif username != user.username and user_exists(username=username):
                    errors.append('用户名已被使用')

            if errors:
                return {'success': False, 'errors': errors}

            # 更新信息
            allowed_fields = ['username', 'email', 'phone']
            for field in allowed_fields:
                if field in profile_data:
                    setattr(user, field, profile_data[field])

            db.session.commit()

            return {
                'success': True,
                'message': '更新成功',
                'user': user.to_dict()
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'更新失败: {str(e)}']}

    @staticmethod
    def change_password(user_id, password_data):
        """修改密码"""
        try:
            user = User.query.get(user_id)
            if not user:
                return {'success': False, 'errors': ['用户不存在']}

            old_password = password_data.get('old_password')
            new_password = password_data.get('new_password')

            if not old_password or not new_password:
                return {'success': False, 'errors': ['请提供旧密码和新密码']}

            if len(new_password) < 6:
                return {'success': False, 'errors': ['新密码至少6个字符']}

            # 验证旧密码
            if not user.check_password(old_password):
                return {'success': False, 'errors': ['旧密码错误']}

            # 更新密码
            user.set_password(new_password)
            db.session.commit()

            return {
                'success': True,
                'message': '密码修改成功'
            }

        except Exception as e:
            db.session.rollback()
            return {'success': False, 'errors': [f'密码修改失败: {str(e)}']}

    @staticmethod
    def logout_user():
        """用户登出"""
        # 在JWT中，服务端不需要存储token，登出主要在客户端处理
        # 可以在这里添加黑名单机制等
        return {'success': True, 'message': '登出成功'}