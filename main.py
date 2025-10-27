import sqlite3
from datetime import datetime


class DatabaseManager:
	def __init__(self, db_name='shop.db'):
		self.db_name = db_name
		self.connection = None

	def connect(self):
		try:
			self.connection = sqlite3.connect(self.db_name)
			self.connection.row_factory = sqlite3.Row
			self.connection.execute('PRAGMA foreign_keys = ON')
			print("Успешное подключение к базе данных")
		except sqlite3.Error as e:
			print(f"Ошибка подключения: {e}")

	def disconnect(self):
		if self.connection:
			self.connection.close()
			print("Соединение с базой данных закрыто")

	def execute_query(self, query, params=None):
		try:
			cursor = self.connection.cursor()
			if params:
				cursor.execute(query, params)
			else:
				cursor.execute(query)
			self.connection.commit()
			return cursor
		except sqlite3.Error as e:
			print(f"Ошибка выполнения запроса: {e}")
			return None

	def create_tables(self):
		queries = [
			"""
			CREATE TABLE IF NOT EXISTS categories (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name VARCHAR(100) NOT NULL,
				description TEXT,
				created_at DATETIME DEFAULT CURRENT_TIMESTAMP
			)
			""",
			"""
			CREATE TABLE IF NOT EXISTS products (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				name VARCHAR(200) NOT NULL,
				description TEXT,
				price DECIMAL(10, 2) NOT NULL,
				category_id INTEGER,
				stock_quantity INTEGER DEFAULT 0,
				created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
				FOREIGN KEY (category_id) REFERENCES categories(id)
			)
			""",
			"""
			CREATE TABLE IF NOT EXISTS customers (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				first_name VARCHAR(100) NOT NULL,
				last_name VARCHAR(100) NOT NULL,
				email VARCHAR(150) UNIQUE NOT NULL,
				phone VARCHAR(20),
				registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
			)
			""",
			"""
			CREATE TABLE IF NOT EXISTS orders (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				customer_id INTEGER NOT NULL,
				order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
				total_amount DECIMAL(10, 2) NOT NULL,
				status VARCHAR(50) DEFAULT 'pending',
				FOREIGN KEY (customer_id) REFERENCES customers(id)
			)
			""",
			"""
			CREATE TABLE IF NOT EXISTS order_items (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				order_id INTEGER NOT NULL,
				product_id INTEGER NOT NULL,
				quantity INTEGER NOT NULL,
				unit_price DECIMAL(10, 2) NOT NULL,
				FOREIGN KEY (order_id) REFERENCES orders(id),
				FOREIGN KEY (product_id) REFERENCES products(id)
			)
			"""
		]
		for q in queries:
			self.execute_query(q)
		print("Таблицы созданы")

	def insert_sample_data(self):
		categories = [
			('Электроника', 'Смартфоны, ноутбуки, планшеты и другие гаджеты'),
			('Одежда', 'Мужская, женская и детская одежда'),
			('Книги', 'Художественная и учебная литература'),
			('Дом и сад', 'Товары для дома и садоводства')
		]
		for c in categories:
			self.execute_query("INSERT INTO categories (name, description) VALUES (?, ?)", c)

		products = [
			('iPhone 14', 'Смартфон Apple iPhone 14 128GB', 799.99, 1, 50),
			('Samsung Galaxy S23', 'Смартфон Samsung Galaxy S23 256GB', 749.99, 1, 30),
			('Футболка хлопковая', 'Хлопковая футболка унисекс', 19.99, 2, 100),
			('Джинсы классические', 'Классические джинсы синего цвета', 49.99, 2, 75),
			('Война и мир', 'Роман Льва Толстого', 24.99, 3, 25),
			('Горшок цветочный', 'Керамический горшок для цветов', 12.99, 4, 200)
		]
		for p in products:
			self.execute_query(
				"INSERT INTO products (name, description, price, category_id, stock_quantity) VALUES (?, ?, ?, ?, ?)",
				p
			)

		customers = [
			('Иван', 'Петров', 'ivan.petrov@email.com', '+7-123-456-7890'),
			('Мария', 'Сидорова', 'maria.sidorova@email.com', '+7-987-654-3210'),
			('Алексей', 'Козлов', 'alexey.kozlov@email.com', '+7-555-123-4567')
		]
		for cust in customers:
			self.execute_query(
				"INSERT INTO customers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
				cust
			)

		orders = [
			(1, 819.98, 'completed'),
			(2, 69.98, 'pending'),
			(3, 24.99, 'shipped')
		]
		for o in orders:
			self.execute_query(
				"INSERT INTO orders (customer_id, total_amount, status) VALUES (?, ?, ?)",
				o
			)

		order_items = [
			(1, 1, 1, 799.99),
			(1, 3, 1, 19.99),
			(2, 3, 2, 19.99),
			(2, 4, 1, 29.99),
			(3, 5, 1, 24.99)
		]
		for oi in order_items:
			self.execute_query(
				"INSERT INTO order_items (order_id, product_id, quantity, unit_price) VALUES (?, ?, ?, ?)",
				oi
			)
		print("Тестовые данные добавлены")

	def get_products_by_category(self, category_id):
		query = """
        SELECT p.name, p.price, p.stock_quantity, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.category_id = ?
        ORDER BY p.price DESC
        """
		cur = self.execute_query(query, (category_id,))
		return cur.fetchall() if cur else []

	def get_expensive_products(self, min_price=500):
		query = """
        SELECT p.name, p.price, c.name as category_name
        FROM products p
        JOIN categories c ON p.category_id = c.id
        WHERE p.price > ?
        ORDER BY p.price DESC
        """
		cur = self.execute_query(query, (min_price,))
		return cur.fetchall() if cur else []

	def get_product_statistics(self):
		queries = {
			'total_products': "SELECT COUNT(*) AS count FROM products",
			'total_categories': "SELECT COUNT(*) AS count FROM categories",
			'avg_price': "SELECT AVG(price) AS avg_price FROM products",
			'total_stock': "SELECT SUM(stock_quantity) AS total FROM products"
		}
		stats = {}
		for k, q in queries.items():
			cur = self.execute_query(q)
			stats[k] = (cur.fetchone()[0] if cur else 0)
		return stats

	def update_product_price(self, product_id, new_price):
		self.execute_query("UPDATE products SET price = ? WHERE id = ?", (new_price, product_id))
		print(f"Цена продукта {product_id} обновлена")

	def delete_product(self, product_id):
		self.execute_query("DELETE FROM products WHERE id = ?", (product_id,))
		print(f"Продукт {product_id} удален")


def main():
	db = DatabaseManager()
	db.connect()
	db.create_tables()
	db.insert_sample_data()

	print("\n=== Продукты категории 'Электроника' ===")
	for product in db.get_products_by_category(1):
		print(f"{product['name']} - ${product['price']} (в наличии: {product['stock_quantity']})")

	print("\n=== Дорогие продукты (> $500) ===")
	for product in db.get_expensive_products(500):
		print(f"{product['name']} - ${product['price']} ({product['category_name']})")

	print("\n=== Статистика магазина ===")
	stats = db.get_product_statistics()
	print(f"Всего продуктов: {stats['total_products']}")
	print(f"Всего категорий: {stats['total_categories']}")
	print(f"Средняя цена: ${stats['avg_price']:.2f}")
	print(f"Общее количество на складе: {stats['total_stock']}")

	db.update_product_price(1, 849.99)
	db.disconnect()


if __name__ == "__main__":
	main()
