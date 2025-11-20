-- 咖啡点餐管理系统数据库结构
-- 创建数据库
CREATE DATABASE IF NOT EXISTS coffee_ordering_system CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE coffee_ordering_system;

-- 用户表
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_username (username),
    INDEX idx_email (email)
);

-- 菜单表
CREATE TABLE menu (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category VARCHAR(50) NOT NULL DEFAULT 'coffee',
    image_url VARCHAR(255),
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_available (is_available)
);

-- 订单表
CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    total_price DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'preparing', 'ready', 'completed', 'cancelled') DEFAULT 'pending',
    customer_name VARCHAR(100),
    customer_phone VARCHAR(20),
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_order_number (order_number),
    INDEX idx_created_at (created_at)
);

-- 订单明细表
CREATE TABLE order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_id INT NOT NULL,
    quantity INT NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    subtotal DECIMAL(10,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_id) REFERENCES menu(id) ON DELETE RESTRICT,
    INDEX idx_order_id (order_id),
    INDEX idx_menu_id (menu_id)
);

-- 插入管理员默认账户 (密码: admin123)
INSERT INTO users (username, email, password, role, phone) VALUES
('admin', 'admin@coffee.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFu6JsygKJrnZvK', 'admin', '13800138000');

-- 插入示例菜单数据
INSERT INTO menu (name, description, price, category, image_url, is_available) VALUES
('美式咖啡', '经典美式咖啡，口感浓郁醇厚', 18.00, 'coffee', '/images/americano.jpg', TRUE),
('拿铁咖啡', '意式浓缩咖啡配蒸汽牛奶，口感顺滑', 22.00, 'coffee', '/images/latte.jpg', TRUE),
('卡布奇诺', '浓缩咖啡、蒸汽牛奶和奶泡的完美组合', 24.00, 'coffee', '/images/cappuccino.jpg', TRUE),
('摩卡咖啡', '巧克力与咖啡的完美融合', 26.00, 'coffee', '/images/mocha.jpg', TRUE),
('焦糖玛奇朵', '香草糖浆和焦糖酱的甜蜜点缀', 28.00, 'coffee', '/images/macchiato.jpg', TRUE),
('抹茶拿铁', '日式抹茶与牛奶的清新搭配', 25.00, 'tea', '/images/matcha.jpg', TRUE),
('蓝莓松饼', '新鲜蓝莓制作的松软松饼', 15.00, 'pastry', '/images/blueberry-muffin.jpg', TRUE),
('巧克力蛋糕', '浓郁巧克力蛋糕，甜而不腻', 20.00, 'pastry', '/images/chocolate-cake.jpg', TRUE),
('三明治', '新鲜蔬菜和优质肉类制作', 32.00, 'sandwich', '/images/sandwich.jpg', TRUE),
('橙汁', '鲜榨橙汁，维C丰富', 12.00, 'juice', '/images/orange-juice.jpg', TRUE);

-- 创建视图：订单详情视图
CREATE VIEW order_details_view AS
SELECT
    o.id,
    o.order_number,
    o.user_id,
    u.username,
    u.email,
    o.total_price,
    o.status,
    o.customer_name,
    o.customer_phone,
    o.notes,
    o.created_at,
    o.updated_at,
    COUNT(oi.id) as item_count,
    GROUP_CONCAT(
        CONCAT(m.name, ' x', oi.quantity, ' (¥', oi.unit_price, ')')
        SEPARATOR ', '
    ) as items_summary
FROM orders o
LEFT JOIN users u ON o.user_id = u.id
LEFT JOIN order_items oi ON o.id = oi.order_id
LEFT JOIN menu m ON oi.menu_id = m.id
GROUP BY o.id;

-- 创建存储过程：生成订单号
DELIMITER //
CREATE PROCEDURE generate_order_number()
BEGIN
    DECLARE order_num VARCHAR(50);
    DECLARE date_prefix VARCHAR(8);
    SET date_prefix = DATE_FORMAT(NOW(), '%Y%m%d');

    SELECT CONCAT('CO', date_prefix, LPAD(IFNULL(MAX(CAST(SUBSTRING(order_number, -4) AS UNSIGNED)), 0) + 1, 4, '0'))
    INTO order_num
    FROM orders
    WHERE order_number LIKE CONCAT('CO', date_prefix, '%');

    SELECT order_num;
END //
DELIMITER ;