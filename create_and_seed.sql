PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(200) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL,
    category_id INTEGER,
    stock_quantity INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

CREATE TABLE IF NOT EXISTS customers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    phone VARCHAR(20),
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS orders (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id INTEGER NOT NULL,
    order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    total_amount DECIMAL(10,2) NOT NULL,
    status VARCHAR(50) DEFAULT 'pending',
    FOREIGN KEY (customer_id) REFERENCES customers(id)
);

CREATE TABLE IF NOT EXISTS order_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL,
    unit_price DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (order_id) REFERENCES orders(id),
    FOREIGN KEY (product_id) REFERENCES products(id)
);

INSERT INTO categories (name, description) VALUES
('Электроника', 'Смартфоны, ноутбуки, планшеты и другие гаджеты'),
('Одежда', 'Мужская, женская и детская одежда'),
('Книги', 'Художественная и учебная литература'),
('Дом и сад', 'Товары для дома и садоводства');

INSERT INTO products (name, description, price, category_id, stock_quantity) VALUES
('iPhone 14', 'Смартфон Apple iPhone 14 128GB', 799.99, 1, 50),
('Samsung Galaxy S23', 'Смартфон Samsung Galaxy S23 256GB', 749.99, 1, 30),
('Футболка хлопковая', 'Хлопковая футболка унисекс', 19.99, 2, 100),
('Джинсы классические', 'Классические джинсы синего цвета', 49.99, 2, 75),
('Война и мир', 'Роман Льва Толстого', 24.99, 3, 25),
('Горшок цветочный', 'Керамический горшок для цветов', 12.99, 4, 200);

INSERT INTO customers (first_name, last_name, email, phone) VALUES
('Иван', 'Петров', 'ivan.petrov@email.com', '+7-123-456-7890'),
('Мария', 'Сидорова', 'maria.sidorova@email.com', '+7-987-654-3210'),
('Алексей', 'Козлов', 'alexey.kozlov@email.com', '+7-555-123-4567');

INSERT INTO orders (customer_id, total_amount, status) VALUES
(1, 819.98, 'completed'),
(2, 69.98, 'pending'),
(3, 24.99, 'shipped');

INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES
(1, 1, 1, 799.99),
(1, 3, 1, 19.99),
(2, 3, 2, 19.99),
(2, 4, 1, 29.99),
(3, 5, 1, 24.99);
