SELECT * FROM products WHERE price BETWEEN 10 AND 100;
SELECT * FROM products WHERE category_id IN (1, 2);
SELECT * FROM products WHERE name LIKE '%phone%';

SELECT p.name AS product_name, p.price, c.name AS category_name
FROM products p
JOIN categories c ON p.category_id = c.id;

SELECT c.name, COUNT(p.id) AS product_count
FROM categories c
LEFT JOIN products p ON c.id = p.category_id
GROUP BY c.id, c.name
HAVING COUNT(p.id) > 0;
