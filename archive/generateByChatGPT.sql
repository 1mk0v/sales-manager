-- Insert data into offices
INSERT INTO offices ("location") VALUES 
('New York'), 
('Los Angeles'), 
('Chicago'), 
('Houston'), 
('Phoenix'), 
('San Francisco'), 
('Seattle'), 
('Boston'), 
('Miami'), 
('Denver');

-- Insert data into managers
INSERT INTO managers ("name", "surename", "patronomic", "office_id", "role") VALUES 
('John', 'Doe', 'William', 1, 'manager'), 
('Jane', 'Smith', 'Anne', 2, 'manager'),
('Mike', 'Brown', 'Anthony', 3, 'manager'), 
('Sara', 'Johnson', 'Lee', 4, 'administrator'), 
('Chris', 'Davis', 'Paul', 5, 'manager'), 
('Anna', 'Miller', 'Marie', 6, 'manager'), 
('James', 'Wilson', 'Frank', 7, 'administrator'), 
('Emily', 'Moore', 'Kate', 8, 'manager'), 
('David', 'Taylor', 'George', 9, 'manager'), 
('Sophia', 'Anderson', 'Rose', 10, 'manager'),
('Liam', 'Walker', 'John', 1, 'manager'),
('Emma', 'Hall', 'Jane', 2, 'administrator'),
('Noah', 'Scott', 'Peter', 3, 'manager'),
('Olivia', 'King', 'Anna', 4, 'administrator'),
('William', 'Green', 'Arthur', 5, 'manager'),
('Ava', 'Adams', 'Elizabeth', 6, 'administrator'),
('James', 'Hill', 'Christopher', 7, 'manager'),
('Sophia', 'Baker', 'Grace', 8, 'administrator'),
('Benjamin', 'Campbell', 'Henry', 9, 'manager'),
('Isabella', 'Mitchell', 'Olivia', 10, 'administrator'),
('Lucas', 'Carter', 'James', 1, 'manager'),
('Mia', 'Roberts', 'Sophia', 2, 'administrator'),
('Henry', 'Phillips', 'Oliver', 3, 'manager'),
('Charlotte', 'Turner', 'Victoria', 4, 'administrator'),
('Alexander', 'Parker', 'William', 5, 'manager'),
('Amelia', 'Evans', 'Emma', 6, 'administrator'),
('Ethan', 'Edwards', 'Liam', 7, 'manager'),
('Harper', 'Collins', 'Mia', 8, 'administrator'),
('Daniel', 'Stewart', 'Lucas', 9, 'manager'),
('Evelyn', 'Morris', 'Charlotte', 10, 'administrator'),
('Matthew', 'Harris', 'Benjamin', 1, 'manager'),
('Ella', 'Clark', 'Harper', 2, 'administrator'),
('Joseph', 'Ramirez', 'Alexander', 3, 'manager'),
('Luna', 'Martinez', 'Evelyn', 4, 'administrator'),
('Michael', 'Lewis', 'Daniel', 5, 'manager'),
('Aria', 'Lee', 'Matthew', 6, 'administrator'),
('Andrew', 'Walker', 'Michael', 7, 'manager'),
('Scarlett', 'Young', 'Ella', 8, 'administrator'),
('Samuel', 'Allen', 'Joseph', 9, 'manager'),
('Victoria', 'Hernandez', 'Luna', 10, 'administrator');

-- Insert data into user_auth
INSERT INTO user_auth ("login", "password_hash", "user_id") VALUES 
('johndoe', '$2b$12$gOvuOdcyiNR6g1ky4bB.z.ZxCptBh1UAEoABf83inl0Rp.fynE5LC', 1), 
('janesmith', '$2b$12$LLH5Mcp54dTkqCyK0bdFLeA21qTybBaA.UE0Tgaff4KvrkP576ETa', 2), 
('mikebrown', '$2b$12$cyMNp7SDM.I9.wgN0XdzlO/9/FHNhKKGlJzssrvkVBtBOEVPNSzwe', 3), 
('sarajohnson', '$2b$12$J1nPjmprR19vL3rbn4415ONHBVtlAeRAeI6ykpCR4XBrW8SHG.wHe', 4), 
('chrisdavis', '$2b$12$c.9W.n.flucpuqOtEUVQqe6.n3kuS3MjL3.GIvys2IDKwMBJYJ8Pq', 5), 
('annamiller', '$2b$12$S6m4oR4y8B0Vom39j4RKxujuuTHY1E2HJ9S8cmHSpfdwZxsjIfEdO', 6), 
('jameswilson', '$2b$12$Y1TpvAddvuxXndn6jdgqquMgGKsyeNWyXqxtr7lS33yqQxVR57q6S', 7), 
('emilymoore', '$2b$12$3DgQQUK4US7KnnKZeyNQxudisTmB0y6sZF3ztfvWcIKgU1S92GmVS', 8), 
('davidtaylor', '$2b$12$WcOsh3g6X3IJJ.JeOYjhqurRNm2peZjwIF19dphlJDyiNA4j9dEqW', 9), 
('sophiaanderson', '$2b$12$SauikDqqVck6UZsGJ1/P6edEgMUj500scUwuqafn45tYu.hKsM83y', 10);

-- Insert data into customers
INSERT INTO customers ("name", "email", "dt_reg", "manag_id", "sex") VALUES 
('Alice', 'alice@example.com', '2024-01-15', 1, 'F'), 
('Bob', 'bob@example.com', '2024-02-20', 2, 'M'), 
('Charlie', 'charlie@example.com', '2024-03-10', 3, 'M'), 
('Diana', 'diana@example.com', '2024-04-05', 4, 'F'), 
('Edward', 'edward@example.com', '2024-05-25', 5, 'M'), 
('Fiona', 'fiona@example.com', '2024-06-18', 6, 'F'),
('George', 'george@example.com', '2024-07-09', 7, 'M'),
('Hannah', 'hannah@example.com', '2024-08-12', 8, 'F'), 
('Isaac', 'isaac@example.com', '2024-09-23', 9, 'M'), 
('Julia', 'julia@example.com', '2024-10-30', 10, 'F');

-- Insert data into office_heads
INSERT INTO office_heads ("office_id", "manag_id") VALUES 
(1, 1),
(1, 1);

-- Insert data into products
INSERT INTO products ("name", "category", "price") VALUES 
('Laptop', 'Electronics', 1200.00), 
('Smartphone', 'Electronics', 800.00), 
('Tablet', 'Electronics', 400.00), 
('Printer', 'Office Supplies', 150.00), 
('Desk', 'Furniture', 300.00), 
('Chair', 'Furniture', 100.00), 
('Monitor', 'Electronics', 250.00), 
('Keyboard', 'Electronics', 50.00), 
('Mouse', 'Electronics', 25.00), 
('Headphones', 'Electronics', 75.00);

-- Insert data into reviews
INSERT INTO reviews ("dt_rep", "cust_id", "manag_id", "result") VALUES 
('2024-11-01', 1, 1, 5), 
('2024-11-02', 2, 2, 4), 
('2024-11-03', 3, 3, 3), 
('2024-11-04', 4, 4, 5), 
('2024-11-05', 5, 5, 2), 
('2024-11-06', 6, 6, 4), 
('2024-11-07', 7, 7, 5), 
('2024-11-08', 8, 8, 3), 
('2024-11-09', 9, 9, 4), 
('2024-11-10', 10, 10, 5);

-- Insert data into plans
INSERT INTO plans ("dt_rep", "manag_id", "office_id", "category", "plan") VALUES 
('2024-12-01', 1, 1, 'Sales_amount', 50000.00), 
('2024-12-02', 2, 2, 'Sales_amount', 30000.00), 
('2024-12-03', 3, 3, 'Sales_amount', 20000.00), 
('2024-12-04', 4, 4, 'New_cln', 40), 
('2024-12-05', 5, 5, 'New_cln', 35), 
('2024-12-06', 6, 6, 'New_cln', 45), 
('2024-12-07', 7, 7, 'New_cln', 50), 
('2024-12-08', 8, 8, 'Sales_amount', 30000.00), 
('2024-12-09', 9, 9, 'Sales_amount', 20000.00), 
('2024-12-10', 10, 10, 'Sales_amount', 40000.00);

-- Insert data into sales
INSERT INTO sales ("dt_rep", "cust_id", "office_id", "manag_id", "prod_id", "amount", "cnt") VALUES 
('2024-12-01', 1, 1, 1, 1, 2400.00, 2), 
('2024-12-02', 2, 2, 2, 2, 1600.00, 2), 
('2024-12-03', 3, 3, 3, 3, 400.00, 1), 
('2024-12-04', 4, 4, 4, 4, 150.00, 1), 
('2024-12-05', 5, 5, 5, 5, 900.00, 3), 
('2024-12-06', 6, 6, 6, 6, 250.00, 1), 
('2024-12-06', 7, 7, 7, 7, 50.00, 1), 
('2024-12-06', 8, 8, 8, 8, 25.00, 1), 
('2024-12-05', 9, 9, 9, 9, 75.00, 1), 
('2024-12-02', 10, 10, 10, 10, 300.00, 4),
('2024-12-11', 3, 2, 2, 1, 2400.00, 2),
('2024-12-11', 4, 3, 3, 2, 800.00, 1),
('2024-12-13', 5, 4, 4, 4, 450.00, 3),
('2024-12-13', 6, 5, 5, 5, 600.00, 2),
('2024-12-15', 7, 6, 6, 6, 750.00, 3),
('2024-12-15', 8, 7, 7, 7, 350.00, 5),
('2024-12-17', 9, 8, 8, 8, 125.00, 1),
('2024-12-18', 10, 9, 9, 9, 300.00, 4),
('2024-12-20', 1, 10, 10, 10, 900.00, 3),
('2024-12-20', 2, 1, 1, 1, 4800.00, 4);
