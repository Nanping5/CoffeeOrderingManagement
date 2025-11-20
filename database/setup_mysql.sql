-- MySQL 数据库设置脚本
-- 请在MySQL命令行中执行此脚本来创建数据库

-- 创建数据库
CREATE DATABASE IF NOT EXISTS coffee_ordering
DEFAULT CHARACTER SET utf8mb4
DEFAULT COLLATE utf8mb4_unicode_ci;

-- 使用数据库
USE coffee_ordering;

-- 创建用户（如果需要创建新用户）
-- CREATE USER IF NOT EXISTS 'coffee_user'@'localhost' IDENTIFIED BY 'your_password';
-- GRANT ALL PRIVILEGES ON coffee_ordering.* TO 'coffee_user'@'localhost';
-- FLUSH PRIVILEGES;

-- 设置root用户密码（如果还没有设置）
-- ALTER USER 'root'@'localhost' IDENTIFIED BY 'your_password';
-- FLUSH PRIVILEGES;

-- 显示数据库信息
SELECT DATABASE() AS 'Current Database';
SELECT 'Database created successfully!' AS 'Status';