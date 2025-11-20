#!/usr/bin/env python3
"""
测试MySQL数据库连接
"""
import pymysql
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

def test_mysql_connection():
    """测试MySQL数据库连接"""
    try:
        # 从环境变量获取数据库URL
        database_url = os.getenv('DATABASE_URL')
        print(f"测试数据库连接: {database_url}")

        # 解析数据库URL
        if database_url.startswith('mysql+pymysql://'):
            # 移除mysql+pymysql://前缀
            db_url = database_url.replace('mysql+pymysql://', '')

            # 解析连接参数
            if '@' in db_url:
                auth_part, host_part = db_url.split('@')
                if ':' in auth_part:
                    username, password = auth_part.split(':', 1)
                else:
                    username = auth_part
                    password = ''

                if '/' in host_part:
                    host_db = host_part.split('/')
                    host_port = host_db[0]
                    database = host_db[1] if len(host_db) > 1 else ''

                    if ':' in host_port:
                        host, port = host_port.split(':')
                        port = int(port)
                    else:
                        host = host_port
                        port = 3306
                else:
                    host = host_part
                    port = 3306
                    database = ''
            else:
                print("无法解析数据库URL")
                return False
        else:
            print("不支持的数据库类型")
            return False

        # 测试连接
        print(f"连接参数:")
        print(f"  主机: {host}")
        print(f"  端口: {port}")
        print(f"  用户: {username}")
        print(f"  密码: {'*' * len(password) if password else '(空)'}")
        print(f"  数据库: {database}")

        # 尝试连接
        connection = pymysql.connect(
            host=host,
            port=port,
            user=username,
            password=password,
            database=database,
            charset='utf8mb4',
            connect_timeout=10
        )

        print("MySQL连接成功!")

        # 测试基本查询
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION()")
            version = cursor.fetchone()
            print(f"MySQL版本: {version[0]}")

            cursor.execute("SELECT DATABASE()")
            current_db = cursor.fetchone()
            print(f"当前数据库: {current_db[0]}")

        connection.close()
        return True

    except Exception as e:
        print(f"MySQL连接失败: {e}")
        return False

if __name__ == "__main__":
    test_mysql_connection()