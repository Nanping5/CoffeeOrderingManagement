#!/usr/bin/env python3
"""
创建数据库表和初始数据的脚本
"""
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
import pymysql

# 加载环境变量
load_dotenv()

def create_database_if_not_exists():
    """创建数据库（如果不存在）"""
    try:
        # 连接MySQL（不指定数据库）
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='060311',
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        # 创建数据库
        cursor.execute("""
            CREATE DATABASE IF NOT EXISTS coffee_ordering
            DEFAULT CHARACTER SET utf8mb4
            DEFAULT COLLATE utf8mb4_unicode_ci
        """)

        print("数据库 'coffee_ordering' 创建成功")

        cursor.close()
        connection.close()
        return True

    except Exception as e:
        print(f"创建数据库失败: {e}")
        return False

def create_tables():
    """创建数据库表"""
    try:
        # 读取SQL文件
        with open('../database/schema_simple.sql', 'r', encoding='utf-8') as f:
            schema_sql = f.read()

        # 连接到数据库
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='060311',
            database='coffee_ordering',
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        # 分割并执行SQL语句
        statements = [s.strip() for s in schema_sql.split(';') if s.strip()]

        for statement in statements:
            if statement:
                try:
                    cursor.execute(statement)
                except Exception as e:
                    print(f"执行语句时出错: {statement}")
                    print(f"错误信息: {e}")

        connection.commit()
        cursor.close()
        connection.close()

        print("数据库表创建成功")
        return True

    except Exception as e:
        print(f"创建表失败: {e}")
        return False

def insert_initial_data():
    """插入初始数据"""
    print("初始数据已包含在 schema_simple.sql 中，无需单独插入")
    return True

def verify_tables():
    """验证表是否创建成功"""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='060311',
            database='coffee_ordering',
            charset='utf8mb4'
        )

        cursor = connection.cursor()

        # 查看所有表
        cursor.execute("SHOW TABLES")
        tables = cursor.fetchall()

        print("数据库表列表:")
        for table in tables:
            table_name = table[0]
            print(f"  - {table_name}")

            # 查看表中的记录数
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"    记录数: {count}")

        cursor.close()
        connection.close()

        print(f"\n数据库验证完成，共 {len(tables)} 个表")
        return True

    except Exception as e:
        print(f"验证表失败: {e}")
        return False

def main():
    """主函数"""
    print("开始创建数据库表和初始数据...")
    print("=" * 50)

    # 1. 创建数据库
    if not create_database_if_not_exists():
        return False

    # 2. 创建表
    if not create_tables():
        return False

    # 3. 插入初始数据
    if not insert_initial_data():
        return False

    # 4. 验证结果
    if not verify_tables():
        return False

    print("=" * 50)
    print("数据库设置完成！")
    print("\n现在您可以启动应用了。")
    print("后端地址: http://localhost:5000")
    print("前端地址: http://localhost:3001")

if __name__ == "__main__":
    main()