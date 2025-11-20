"""运行脚本"""
import os
from app import create_app, db
from flask_migrate import upgrade

def deploy():
    """部署函数"""
    # 创建数据库表
    upgrade()

if __name__ == '__main__':
    app = create_app()

    with app.app_context():
        # 确保所有表都已创建
        db.create_all()
        print("数据库表已创建")

    # 启动应用
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=app.config.get('DEBUG', True)
    )