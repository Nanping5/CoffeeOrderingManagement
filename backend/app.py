"""咖啡点餐管理系统 - Flask应用主文件"""
import os
from flask import Flask, jsonify
from flask_migrate import Migrate
from config import config
from extensions import init_extensions, db

def create_app(config_name=None):
    """应用工厂函数"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'development')

    # 创建Flask应用实例
    app = Flask(__name__, static_folder='public', static_url_path='/static')

    # 加载配置
    app.config.from_object(config[config_name])

    # 初始化扩展
    init_extensions(app)

    # 注册蓝图
    from routes.auth import auth_bp
    from routes.user import user_bp
    from routes.order import order_bp

    # 使用数据库菜单路由
    from routes.menu import menu_bp
    app.register_blueprint(menu_bp, url_prefix='/api/menu')
    print("使用数据库版本的菜单路由")

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(user_bp, url_prefix='/api/users')
    app.register_blueprint(order_bp, url_prefix='/api/orders')

    # 错误处理
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': '资源未找到'}), 404

    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return jsonify({'error': '服务器内部错误'}), 500

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({'error': '请求参数错误'}), 400

    # API根路径
    @app.route('/')
    def index():
        return jsonify({
            'message': '咖啡点餐管理系统API',
            'version': '1.0.0',
            'endpoints': {
                'auth': '/api/auth',
                'users': '/api/users',
                'menu': '/api/menu',
                'orders': '/api/orders'
            }
        })

    @app.route('/api/health')
    def health_check():
        """健康检查接口"""
        try:
            # 检查数据库连接
            from sqlalchemy import text
            db.session.execute(text('SELECT 1'))
            return jsonify({
                'status': 'healthy',
                'database': 'connected',
                'app': 'running'
            })
        except Exception as e:
            return jsonify({
                'status': 'unhealthy',
                'database': 'disconnected',
                'error': str(e)
            }), 500

    return app

# 创建应用实例
app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # 确保数据库表存在
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)