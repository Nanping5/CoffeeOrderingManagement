-- 咖啡点餐管理系统 - 简化的数据库表结构
-- 适用于快速部署和测试

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    role ENUM('admin', 'user') DEFAULT 'user',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 菜单项表
CREATE TABLE IF NOT EXISTS menu_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10, 2) NOT NULL,
    original_price DECIMAL(10, 2),
    category VARCHAR(50) DEFAULT 'coffee',
    image_url VARCHAR(255),
    is_available BOOLEAN DEFAULT TRUE,
    is_popular BOOLEAN DEFAULT FALSE,
    tags JSON,
    order_count INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 订单表
CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_number VARCHAR(50) NOT NULL UNIQUE,
    user_id INT NOT NULL,
    total_price DECIMAL(10, 2) NOT NULL,
    subtotal_price DECIMAL(10, 2) NOT NULL,
    delivery_fee DECIMAL(10, 2) DEFAULT 0.00,
    discount DECIMAL(10, 2) DEFAULT 0.00,
    status ENUM('pending', 'processing', 'delivering', 'completed', 'cancelled') DEFAULT 'pending',
    delivery_address TEXT,
    contact_phone VARCHAR(20),
    remark TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_user_id (user_id),
    INDEX idx_status (status),
    INDEX idx_created_at (created_at)
);

-- 订单明细表
CREATE TABLE IF NOT EXISTS order_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    order_id INT NOT NULL,
    menu_item_id INT NOT NULL,
    quantity INT NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) GENERATED ALWAYS AS (quantity * price) STORED,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (order_id) REFERENCES orders(id) ON DELETE CASCADE,
    FOREIGN KEY (menu_item_id) REFERENCES menu_items(id) ON DELETE CASCADE,
    INDEX idx_order_id (order_id),
    INDEX idx_menu_item_id (menu_item_id)
);

-- 用户表索引
DROP INDEX IF EXISTS idx_users_email ON users;
CREATE INDEX idx_users_email ON users(email);
DROP INDEX IF EXISTS idx_users_username ON users;
CREATE INDEX idx_users_username ON users(username);
DROP INDEX IF EXISTS idx_users_role ON users;
CREATE INDEX idx_users_role ON users(role);

-- 菜单项表索引
DROP INDEX IF EXISTS idx_menu_category ON menu_items;
CREATE INDEX idx_menu_category ON menu_items(category);
DROP INDEX IF EXISTS idx_menu_available ON menu_items;
CREATE INDEX idx_menu_available ON menu_items(is_available);
DROP INDEX IF EXISTS idx_menu_popular ON menu_items;
CREATE INDEX idx_menu_popular ON menu_items(is_popular);

-- 创建默认管理员用户 (密码: admin123)
INSERT INTO users (username, email, password, role) VALUES
('admin', 'admin@coffeetime.com', '$2b$12$LQv3c1yZBWThKZEydxh3eEFp/MpQqAQ1VlftWcxQaM5D.YRzC4b3O5', 'admin')
ON DUPLICATE KEY UPDATE password = VALUES(password);

-- 插入示例菜单数据
INSERT INTO menu_items (name, description, price, original_price, category, image_url, is_available, is_popular, tags, order_count) VALUES
('拿铁咖啡', '浓郁的意式咖啡与丝滑奶泡的完美结合', 28.00, 32.00, 'coffee', '/default-coffee.jpg', TRUE, TRUE, '["经典", "热饮", "意式"]', 156),
('美式咖啡', '醇厚的咖啡豆精华，简单纯粹的美式享受', 22.00, NULL, 'coffee', '/default-coffee.jpg', TRUE, FALSE, '["经典", "美式"]', 89),
('卡布奇诺', '意式浓缩咖啡配上蒸汽牛奶和绵密奶泡', 32.00, NULL, 'coffee', '/default-coffee.jpg', TRUE, TRUE, '["意式", "奶泡"]', 98),
('摩卡咖啡', '咖啡与巧克力的美妙融合，甜美诱人', 35.00, NULL, 'coffee', '/default-coffee.jpg', TRUE, FALSE, '["巧克力", "甜点"]', 76),
('提拉米苏', '经典意大利甜点，马斯卡彭奶酪的浓郁魅力', 28.00, NULL, 'dessert', '/default-coffee.jpg', TRUE, TRUE, '["甜点", "意大利"]', 87),
('芝士蛋糕', '绵密香甜的芝士蛋糕，口感丰富层次分明', 26.00, NULL, 'dessert', '/default-coffee.jpg', TRUE, FALSE, '["蛋糕", "甜品"]', 65),
('抹茶拿铁', '日式抹茶与咖啡的完美融合，清香怡人', 30.00, NULL, 'tea', '/default-coffee.jpg', TRUE, FALSE, '["抹茶", "日式"]', 54),
('乌龙茶', '传统中国茶，清香回甘，健康养生', 18.00, NULL, 'tea', '/default-coffee.jpg', TRUE, FALSE, '["中国茶", "传统"]', 43),
('水果沙拉', '新鲜时令水果，营养搭配丰富', 25.00, NULL, 'other', '/default-coffee.jpg', TRUE, FALSE, '["水果", "健康"]', 32),
('烤面包', '香脆可口的烤面包，配黄油果酱', 12.00, NULL, 'other', '/default-coffee.jpg', TRUE, FALSE, '["面包", "烘焙"]', 156);

-- 订单统计表（可选）
CREATE TABLE IF NOT EXISTS order_statistics (
    id INT AUTO_INCREMENT PRIMARY KEY,
    date DATE NOT NULL,
    total_orders INT DEFAULT 0,
    total_amount DECIMAL(12, 2) DEFAULT 0.00,
    completed_orders INT DEFAULT 0,
    cancelled_orders INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    UNIQUE KEY uk_date (date)
);

-- 系统日志表（可选）
CREATE TABLE IF NOT EXISTS system_logs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    action VARCHAR(100) NOT NULL,
    resource VARCHAR(255),
    details TEXT,
    ip_address VARCHAR(45),
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_id (user_id),
    INDEX idx_action (action),
    INDEX idx_created_at (created_at)
);