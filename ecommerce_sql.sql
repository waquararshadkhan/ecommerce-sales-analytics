CREATE DATABASE ecommerce_sales;

USE ecommerce_sales;
SHOW TABLES;
SELECT COUNT(*) FROM sales;
SELECT COUNT(*) FROM sales_target;
SELECT * FROM sales LIMIT 5;

SELECT Category,
       SUM(Amount) AS total_revenue,
       SUM(Profit) AS total_profit,
       COUNT(*) AS num_orders
FROM sales
GROUP BY Category
ORDER BY total_revenue DESC;

SELECT Month, SUM(Amount) AS monthly_revenue
FROM sales
GROUP BY Month
ORDER BY Month;

SELECT State, SUM(Amount) AS total_revenue
FROM sales
GROUP BY State
ORDER BY total_revenue DESC
LIMIT 5;

DESCRIBE sales_target;

SELECT s.Month,
       s.Category,
       SUM(s.Amount) AS actual_revenue,
       t.Target
FROM sales s
JOIN sales_target t
  ON s.Category = t.Category
  AND s.Month = t.`Month of Order Date`
GROUP BY s.Month, s.Category, t.Target
ORDER BY s.Month, s.Category;