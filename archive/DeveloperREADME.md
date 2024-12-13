
# SQL queries for project

## Manager

**!!!ВНИМАНИЕ!!!**
**ВСЕ ЗАПРОСЫ ДЛЯ ОБЫЧНОГО МЕНЕДЖЕРА СОСТАВЛЯЮТСЯ ОТНОСИТЕЛЬНО ЕГО ОФИСА!**
**ЕСЛИ Я ГДЕ-ТО НЕ ПРАВ, ТО ПОПРАВЬТЕ МЕНЯ**

### ВКЛАДКА С ОБЩИМ ДАШБОРДОМ

***Продуктов продано за определенный период***
```sql
-- РАБОТАТЕТ
select SUM(amount) as sold_products from sales where dt_rep >= '2024-11-11' and dt_rep <= '2024-12-11' and manag_id = 1;
```

***План по продажам за определенный период***
```sql
-- РАБОТАТЕТ
select 
    SUM(case when p.category = 'Sales_amount' then p.plan else 0 end) as sales_amount,
    SUM(case when p.category = 'New_cln' then p.plan else 0 end) as new_clients
from "plans" p
where 
    p.dt_rep >= '2024-12-01' 
    and p.dt_rep < '2025-01-01' 
    and p.manag_id = 1;


select p.category, SUM(p.plan) as plan_sum 
from "plans" p
where
	p.dt_rep >= '2024-12-01' 
    and p.dt_rep < '2025-01-01' 
    and p.manag_id = 1
group by p.category;
```

***Эффективность менеджера за определенный период***
```sql
-- тут запрос пожалуйста
-- забыл как считать, но можете мне сюда накидать любые данные, с помощью которых можно посчитать эффективность менеджера
-- если не сложно, то напишите формулу, как надо считац)))))
```

***Ново-привлеченные мною клиенты за определенный период***
```sql
-- ну типо сколько я клиентов привел (количество)
-- РАБОТАТЕТ
select coalesce(count(distinct c.id),0) 
from customers c
where 
	c.dt_reg >= $1
	and c.dt_reg < $2
    and c.manag_id = $3;
```

***Моя выручка***
```sql
-- РАБОТАТЕТ
-- нужно название категории и сумма, на которую удалось продать данную категорию

SELECT p.category, 
    sum(s.amount) as amnt
FROM sales s
join products p
on s.prod_id = p.id
where s.dt_rep >= dt_to and s.dt_rep <= dt_to
and s.manag_id = $1
group by p.category
```

***KPI Execution***
```sql
-- тут запрос пожалуйста
```

***Динамика продаж***
```sql
-- РАБОТАТЕТ
-- тут запрос пожалуйста
-- нужно количество проданных товаров проданных за определенный год (по месяцам)
-- То есть месяц и число продаж в этом месяце
-- Мне тут нужно месяц, в который было совершенны покупки + категория товаров, к которой относились данные товары + сумма проданных товаров
SELECT 
    TO_CHAR(m.month, 'Mon.YY') AS month_sale,
    p.category AS product_category,
    COALESCE(SUM(CASE WHEN s.amount > 0 THEN s.amount ELSE 0 END), 0) AS total_sales
FROM 
    products p
CROSS JOIN 
    (SELECT DISTINCT DATE_TRUNC('month', dt_rep) AS month
     FROM sales 
     WHERE EXTRACT(YEAR FROM dt_rep) = 2024 AND manag_id = 1) m
LEFT JOIN 
    sales s ON p.id = s.prod_id 
              AND DATE_TRUNC('month', s.dt_rep) = m.month  
              AND s.manag_id = 1  
GROUP BY 
    month_sale, p.category
ORDER BY 
    month_sale, p.category;
```

***Популярный товар***
```sql
-- тут запрос пожалуйста
-- Нужно название товара и ссылка на его картинку + количество покупок данного товара (можно штучно или сумма)
```

***Таблица клиентов менеджера***
```sql
-- РАБОТАТЕТ
-- нужно фио клиента, его дата регистрации, дата покупки, продукт который купил, сумма продажи

SELECT s.dt_rep 	as "DT SALE",
	   c.name		as "CLIENT",
	   c.sex		as "SEX",
	   c.dt_reg 	as "DT REG",
	   p.name		as "GOOD",
	   s.amount 	as "TOTAL",
	   s.cnt		as "CNT TOTAL"
FROM sales s
JOIN customers as c ON s.cust_id = c.id
JOIN products as p ON s.prod_id = p.id 
WHERE s.manag_id = 1;
```



### ВКЛАДКА С ТОВАРАМИ

***Популярность категорий***
```sql
-- тут запрос пожалуйста
-- категория + на какую сумму товара продали из данной категории
```

***ТОП 5 лучших продаваемых категорий***
```sql
-- тут запрос пожалуйста
-- категория + на какую сумму товара продали из данной категории
```

***ТОП 5 худших продаваемых категорий***
```sql
-- тут запрос пожалуйста
-- категория + на какую сумму товара продали из данной категории
```

***Таблица ПРОДУКТОВ***
```sql
-- тут запрос пожалуйста
-- имя товара + количество на складе + месяц, в который было совершенны покупки данного товара + сумма проданных товаров в определенном месяце
```


### ВКЛАДКА С КЛИЕНТАМИ

***Конвертация посетителя в покупателя***
```sql
-- РАБОТАТЕТ
-- тут запрос пожалуйста
-- количество клиентов, которое пришло в магазин + количество клиентов, которое что-то купило в магазине
WITH b1 AS (  -- Продажи новым клиентам
    SELECT COUNT(*) AS cnt_cust_1
    FROM customers c
    WHERE EXISTS (
        SELECT 1 
        FROM sales s 
        WHERE s.cust_id = c.id 
          AND s.dt_rep >= '2024-12-01' AND s.dt_rep <= '2025-01-01'
		  AND c.manag_id = $1
    )
    AND c.dt_reg >= '2024-12-01' AND c.dt_reg <= '2025-01-01'
),

b2 AS (   -- Всего новых клиентов
    SELECT COUNT(*) AS cnt_cust_2
    FROM customers c
    WHERE c.dt_reg >= '2024-12-01' AND c.dt_reg <= '2024-12-01'
	AND c.manag_id = $1
)

SELECT 
    b1.cnt_cust_1  		as sales_new_cln,
    b2.cnt_cust_2		as new_cln,
    CASE 
        WHEN b2.cnt_cust_2 = 0 THEN 0 
        ELSE (b1.cnt_cust_1::FLOAT / b2.cnt_cust_2) * 100
    END AS conversion_rate  -- Доля новых клиентов
FROM b2, b1;
```


***CLTV***
```sql
-- РАБОТАТЕТ
-- тут запрос пожалуйста
-- Не помню что это, но по графику, тут должна быть цифра какая-то
WITH cust_stats AS (
    SELECT
        cust_id,
        SUM(amount) AS total_revenue,
        COUNT(sale_id) AS total_purchases,
        MIN(dt_rep) AS first_purchase_date,
        MAX(dt_rep) AS last_purchase_date
    FROM
        sales
    WHERE
        dt_rep >= dt_from AND sale_date <= dt_to
        and manag_id = $1 
        
    GROUP BY
        cust_id
)
SELECT
    cust_id,
    total_revenue,
    total_purchases,
    -- Расчет CLTV
    CASE 
        WHEN total_purchases > 0 THEN total_revenue / total_purchases
        ELSE 0
    END AS cltv
FROM
    customer_stats
```

***Loyality***
```sql
-- тут запрос пожалуйста
-- не помню что это
```

***Клиенты***
```sql
-- РАБОТАТЕТ
-- тут запрос пожалуйста
-- месяц + количество людей, которые купили (или пришли, на ваше усмотрение) в этот месяц + половой признак (м/ж)
WITH baza AS (
    SELECT 
        TO_CHAR(s.dt_rep, 'Mon.YY') 	AS month_sale,
        c.sex 							AS sex,  
        s.cust_id 						AS cust
    FROM 
        sales s
    JOIN customers c 
		ON s.cust_id = c.id
    WHERE 
        EXTRACT(YEAR FROM s.dt_rep) = 2024
		AND s.manag_id = $1
    GROUP BY 
        month_sale, c.sex, s.cust_id  
)
SELECT 
    month_sale,
    sex,
    COUNT(DISTINCT cust) AS cnt_cust  
FROM 
    baza
GROUP BY 
    month_sale, sex  
ORDER BY 
    month_sale, sex;
```

***Таблица с клиентами***
```sql
-- РАБОТАТЕТ
-- тут запрос пожалуйста
-- имя клиента + дата регистрации + количество покупок + общая сумма продажи данному клиенту
SELECT c.name   				AS "CLIENT",
	   c.dt_reg 				AS "DT REG",
	   count(distinct s.id) 	AS "CNT SALES",  --ЕСЛИ ЧТО КОЛ-ВО ПОКУПОК ИМЕННО А НЕ CNT ТОВАРА
	   sum(s.amount)			AS "AMNT SALES"	   
FROM Customers c
LEFT JOIN Sales s
	ON c.id = s.cust_id 
WHERE s.manag_id = 1
GROUP BY c.name, c.dt_reg;
```








## Boss

### ВКЛАДКА С ОБЩИМ ДАШБОРДОМ

***Продуктов продано за определенный период***
```sql
-- РАБОТАТЕТ
select SUM(s.amount*s.cnt)
from sales s
where
	s.office_id in (select oh.id from office_heads oh where oh.manag_id = 4)
	and s.dt_rep >= '2024-12-01'
	and s.dt_rep < '2025-01-01';
```

### Топ 5 менеджеров
```sql
-- тут запрос пожалуйста
```

***План по продажам за определенный период***
```sql
-- РАБОТАТЕТ
select 
    SUM(case when p.category = 'Sales_amount' then p.plan else 0 end) as sales_amount,
    SUM(case when p.category = 'New_cln' then p.plan else 0 end) as new_clients
from "plans" p
where 
    p.dt_rep >= '2024-12-01' 
    and p.dt_rep < '2025-01-01' 
    and p.manag_id = 1;


select p.category, SUM(p.plan) as plan_sum 
from "plans" p
where
	p.dt_rep >= '2024-12-01' 
    and p.dt_rep < '2025-01-01' 
    and p.manag_id = 1
group by p.category;
```

***Эффективность менеджера за определенный период***
```sql
-- тут запрос пожалуйста
-- забыл как считать, но можете мне сюда накидать любые данные, с помощью которых можно посчитать эффективность менеджера
-- если не сложно, то напишите формулу, как надо считац)))))
```

***Ново-привлеченные мною клиенты за определенный период***
```sql
-- ну типо сколько я клиентов привел (количество)
-- РАБОТАТЕТ
select coalesce(count(distinct c.id),0) 
from customers c
where 
	c.dt_reg >= $1
	and c.dt_reg < $2
    and c.manag_id = $3;
```

***Моя выручка***
```sql
-- РАБОТАТЕТ
-- нужно название категории и сумма, на которую удалось продать данную категорию

SELECT p.category, 
	   sum(s.amount) as amnt
FROM sales s
join products p
on s.prod_id = p.id
where s.dt_rep >= '2024-12-01' and s.dt_rep <= '2025-01-01'
and s.manag_id = 1
group by p.category;
```

***KPI Execution***
```sql
-- тут запрос пожалуйста
```

***Динамика продаж***
```sql
-- тут запрос пожалуйста
-- нужно количество проданных товаров проданных за определенный год (по месяцам)
-- То есть месяц и число продаж в этом месяце
-- Мне тут нужно месяц, в который было совершенны покупки + категория товаров, к которой относились данные товары + сумма проданных товаров
SELECT 
    TO_CHAR(s.sale_date, 'Mon.YY') AS month,
    p.category AS product_category,
    SUM(s.quantity) AS total_sales
FROM 
    sales s
JOIN 
    products p ON s.product_id = p.id
WHERE 
    EXTRACT(YEAR FROM s.sale_date) = 2024 
GROUP BY 
    month, p.category
ORDER BY 
    month, p.category
```

***Таблица клиентов менеджера***
```sql
-- нужно фио клиента, его дата регистрации, дата покупки, продукт который купил, сумма продажи

SELECT s.dt_sale,
c.cust_name,
C.dt_reg,
P.product_name,
S.income

FROM sales s
JOIN customers c
ON s.cust_id = c.cust_id
JOIN products p
ON c.product_id = p.product_id

SELECT
    p.product_name,
    SUM(s.income) AS total_quantity_sold
FROM
    sales s
JOIN
    products p ON s.product_id = p.product_id
WHERE
    s.sale_date >= dt_FROM AND s.sale_date <= dt_to
GROUP BY
   P.product_name
ORDER BY
    total_quantity_sold DESC
LIMIT 1
```



### ВКЛАДКА С ТОВАРАМИ

***Популярность категорий***
```sql
-- тут запрос пожалуйста
-- категория + на какую сумму товара продали из данной категории
```

***ТОП 5 лучших продаваемых категорий***
```sql
-- тут запрос пожалуйста
-- категория + на какую сумму товара продали из данной категории
```

***ТОП 5 худших продаваемых категорий***
```sql
-- тут запрос пожалуйста
-- категория + на какую сумму товара продали из данной категории
```

***Таблица ПРОДУКТОВ***
```sql
-- тут запрос пожалуйста
-- имя товара + количество на складе + месяц, в который было совершенны покупки данного товара + сумма проданных товаров в определенном месяце
```


### ВКЛАДКА С КЛИЕНТАМИ

***Конвертация посетителя в покупателя***
```sql
-- тут запрос пожалуйста
-- количество клиентов, которое пришло в магазин + количество клиентов, которое что-то купило в магазине
```

***CLTV***
```sql
-- тут запрос пожалуйста
-- Не помню что это, но по графику, тут должна быть цифра какая-то
WITH cust_stats AS (
    SELECT
        cust_id,
        SUM(amount) AS total_revenue,
        COUNT(sale_id) AS total_purchases,
        MIN(dt_rep) AS first_purchase_date,
        MAX(dt_rep) AS last_purchase_date
    FROM
        sales
    WHERE
        dt_rep >= dt_from AND sale_date <= dt_to
        and manag_id = $1 
        
    GROUP BY
        cust_id
)

SELECT
    cust_id,
    total_revenue,
    total_purchases,
    -- Расчет CLTV
    CASE 
        WHEN total_purchases > 0 THEN total_revenue / total_purchases
        ELSE 0
    END AS cltv
FROM
    customer_stats
```

***Loyality***
```sql
-- тут запрос пожалуйста
-- не помню что это
```

***Клиенты***
```sql
-- тут запрос пожалуйста
-- месяц + количество людей, которые купили (или пришли, на ваше усмотрение) в этот месяц + половой признак (м/ж)
```

***Таблица с клиентами***
```sql
-- тут запрос пожалуйста
-- имя клиента + дата регистрации + количество покупок + общая сумма продажи данному клиенту
```