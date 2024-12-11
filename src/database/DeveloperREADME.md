
# SQL queries for project

## Manager

**!!!ВНИМАНИЕ!!!**
**ВСЕ ЗАПРОСЫ ДЛЯ ОБЫЧНОГО МЕНЕДЖЕРА СОСТАВЛЯЮТСЯ ОТНОСИТЕЛЬНО ЕГО ОФИСА!**
**ЕСЛИ Я ГДЕ-ТО НЕ ПРАВ, ТО ПОПРАВЬТЕ МЕНЯ**

### ВКЛАДКА С ОБЩИМ ДАШБОРДОМ

***Продуктов продано за определенный период***
```sql
SELECT Coalesce( count(product), 0) as sale_prod
FROM Sales
WHERE dt_rep >= dt_FROM
AND dt_rep <= dt_to
AND manag_id = $1 
```

***План по продажам за определенный период***
```sql
-- тут запрос пожалуйста
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

SELECT coalesce(count(distinct cust_id), 0)
FROM Sales
WHERE dt_reg >= dt_FROM
AND dt_reg <= dt_to
AND manag_id = $1
```

***Моя выручка***
```sql
-- нужно название категории и сумма, на которую удалось продать данную категорию

SELECT category, sum(income) as revenue
FROM sales
WHERE dt_rep >= dt_FROM
AND dt_rep <= dt_to
AND manag_id = $1
GROUP by category
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

***Популярный товар***
```sql
-- тут запрос пожалуйста
-- Нужно название товара и ссылка на его картинку + количество покупок данного товара (можно штучно или сумма)
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

## Boss

### Топ 5 менеджеров
```sql
-- тут запрос пожалуйста
```
