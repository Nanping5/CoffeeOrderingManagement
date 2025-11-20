-- 咖啡点餐管理系统初始化数据脚本
USE coffee_ordering_system;

-- 创建测试用户账户
INSERT INTO users (username, email, password, role, phone) VALUES
('testuser', 'test@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFu6JsygKJrnZvK', 'user', '13800138001'),
('customer1', 'customer1@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFu6JsygKJrnZvK', 'user', '13800138002'),
('customer2', 'customer2@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewFu6JsygKJrnZvK', 'user', '13800138003');

-- 插入更多菜单项
INSERT INTO menu (name, description, price, category, image_url, is_available) VALUES
('浓缩咖啡', '纯正意式浓缩咖啡，强烈浓郁', 15.00, 'coffee', '/images/espresso.jpg', TRUE),
('康宝蓝', '浓缩咖啡配鲜奶油', 28.00, 'coffee', '/images/con-panna.jpg', TRUE),
('爱尔兰咖啡', '咖啡与威士忌的温暖组合', 35.00, 'coffee', '/images/irish-coffee.jpg', TRUE),
('冰咖啡', '清爽冰镇咖啡，夏日首选', 20.00, 'coffee', '/images/iced-coffee.jpg', TRUE),
('热巧克力', '浓郁热巧克力，温暖甜蜜', 18.00, 'hot', '/images/hot-chocolate.jpg', TRUE),
('柠檬茶', '清新柠檬茶，解渴提神', 16.00, 'tea', '/images/lemon-tea.jpg', TRUE),
('绿茶', '传统中国绿茶，清香回甘', 14.00, 'tea', '/images/green-tea.jpg', TRUE),
('红茶', '醇厚红茶，经典英式风味', 14.00, 'tea', '/images/black-tea.jpg', TRUE),
('羊角面包', '法式经典羊角面包，酥脆可口', 12.00, 'pastry', '/images/croissant.jpg', TRUE),
('甜甜圈', '美式经典甜甜圈，甜而不腻', 10.00, 'pastry', '/images/donut.jpg', TRUE),
('苹果派', '自制苹果派，香甜酥脆', 18.00, 'pastry', '/images/apple-pie.jpg', TRUE),
('芝士蛋糕', '纽约风味芝士蛋糕，口感丰富', 22.00, 'pastry', '/images/cheesecake.jpg', TRUE),
('番茄汁', '新鲜番茄榨汁，酸甜可口', 10.00, 'juice', '/images/tomato-juice.jpg', TRUE),
('苹果汁', '100%纯苹果汁，天然健康', 10.00, 'juice', '/images/apple-juice.jpg', TRUE),
('矿泉水', '天然矿泉水，纯净清爽', 5.00, 'water', '/images/water.jpg', TRUE);

-- 插入一些示例订单（使用存储过程生成订单号）
-- 用户1的第一个订单
CALL generate_order_number();
INSERT INTO orders (user_id, order_number, total_price, status, customer_name, customer_phone, notes) VALUES
(2, 'CO202411200001', 48.00, 'completed', '张三', '13800138001', '少糖少冰');

-- 为第一个订单添加订单项
INSERT INTO order_items (order_id, menu_id, quantity, unit_price, subtotal) VALUES
(1, 2, 1, 22.00, 22.00),  -- 拿铁咖啡
(1, 9, 1, 20.00, 20.00),  -- 巧克力蛋糕
(1, 10, 1, 6.00, 6.00);   -- 橙汁

-- 用户1的第二个订单
CALL generate_order_number();
INSERT INTO orders (user_id, order_number, total_price, status, customer_name, customer_phone, notes) VALUES
(2, 'CO202411200002', 30.00, 'preparing', '张三', '13800138001', '多加糖');

-- 为第二个订单添加订单项
INSERT INTO order_items (order_id, menu_id, quantity, unit_price, subtotal) VALUES
(2, 1, 1, 18.00, 18.00),  -- 美式咖啡
(2, 7, 1, 12.00, 12.00);  -- 蓝莓松饼

-- 用户2的订单
CALL generate_order_number();
INSERT INTO orders (user_id, order_number, total_price, status, customer_name, customer_phone, notes) VALUES
(3, 'CO202411200003', 54.00, 'pending', '李四', '13800138002', '尽快准备');

-- 为第三个订单添加订单项
INSERT INTO order_items (order_id, menu_id, quantity, unit_price, subtotal) VALUES
(3, 3, 2, 24.00, 48.00),  -- 卡布奇诺 x2
(3, 16, 1, 6.00, 6.00);   -- 矿泉水

-- 显示数据统计信息
SELECT '用户统计' as type, COUNT(*) as count FROM users
UNION ALL
SELECT '菜单项统计', COUNT(*) FROM menu
UNION ALL
SELECT '订单统计', COUNT(*) FROM orders
UNION ALL
SELECT '订单项统计', COUNT(*) FROM order_items;

-- 显示用户信息
SELECT id, username, email, role, phone, created_at FROM users;

-- 显示菜单信息（按类别分组）
SELECT category, COUNT(*) as count, AVG(price) as avg_price FROM menu GROUP BY category;

-- 显示订单状态统计
SELECT status, COUNT(*) as count FROM orders GROUP BY status;