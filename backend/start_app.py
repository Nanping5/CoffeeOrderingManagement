"""简化启动脚本"""
import os
from app import create_app
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def main():
    """主函数"""
    print("正在启动咖啡点餐管理系统...")

    # 创建Flask应用
    app = create_app()

    # 先启动应用，数据库表会在访问时自动创建
    print("Flask应用已创建")
    print(f"数据库连接: {os.getenv('DATABASE_URL', '未配置')}")

    # 启动应用
    try:
        app.run(
            host='0.0.0.0',
            port=int(os.environ.get('PORT', 5000)),
            debug=app.config.get('DEBUG', True)
        )
    except Exception as e:
        print(f"启动失败: {e}")
        print("请检查数据库连接配置")

if __name__ == '__main__':
    main()