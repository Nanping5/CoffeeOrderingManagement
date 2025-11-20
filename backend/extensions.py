"""Flask扩展初始化模块"""
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from werkzeug.utils import secure_filename
import os

# 创建扩展实例
db = SQLAlchemy()
migrate = Migrate()
cors = CORS()
jwt = JWTManager()
ma = Marshmallow()
bcrypt = Bcrypt()

def init_extensions(app):
    """初始化所有扩展"""
    # 初始化数据库
    db.init_app(app)
    migrate.init_app(app, db)

    # 初始化CORS
    cors.init_app(app, origins=app.config['CORS_ORIGINS'])

    # 初始化JWT
    jwt.init_app(app)

    # 初始化Marshmallow
    ma.init_app(app)

    # 初始化bcrypt
    bcrypt.init_app(app)

    # 确保上传目录存在
    upload_folder = app.config.get('UPLOAD_FOLDER', 'static/uploads')
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # JWT错误处理
    @jwt.expired_token_loader
    def expired_token_callback(jwt_header, jwt_payload):
        from flask import jsonify
        return jsonify({'message': 'Token已过期'}), 401

    @jwt.invalid_token_loader
    def invalid_token_callback(error):
        from flask import jsonify
        return jsonify({'message': '无效的Token'}), 401

    @jwt.unauthorized_loader
    def missing_token_callback(error):
        from flask import jsonify
        return jsonify({'message': '需要Token'}), 401

def allowed_file(filename, allowed_extensions=None):
    """检查文件扩展名是否被允许"""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_file(file, folder='uploads'):
    """保存上传的文件"""
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        # 添加时间戳避免文件名冲突
        import time
        timestamp = int(time.time())
        filename = f"{timestamp}_{filename}"

        upload_path = os.path.join(folder, filename)
        file.save(upload_path)
        return upload_path
    return None