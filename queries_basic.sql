SELECT * FROM categories;
SELECT name, price FROM products;
SELECT * FROM products WHERE price > 50;
SELECT * FROM products ORDER BY price DESC;
SELECT * FROM products LIMIT 3;

SELECT COUNT(*) AS total_products FROM products;
SELECT AVG(price) AS average_price FROM products;
SELECT MAX(price) AS max_price, MIN(price) AS min_price FROM products;
SELECT SUM(stock_quantity) AS total_stock FROM products;

SELECT c.name, COUNT(p.id) AS product_count
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.name;

SELECT c.name, AVG(p.price) AS avg_price
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.name;
