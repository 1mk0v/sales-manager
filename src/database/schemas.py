offices = (
    """
        id SERIAL PRIMARY KEY,
        location VARCHAR(100)
    """
)

managers = (
    """
        id SERIAL PRIMARY KEY,
        name VARCHAR(20),
        surename VARCHAR(20),
        patronomic VARCHAR(20),
        office_id INTEGER,
        role VARCHAR(20),
        FOREIGN KEY (office_id) REFERENCES offices (id) ON DELETE CASCADE
    """
)

user_auth = (
    """
        login VARCHAR(20) PRIMARY KEY,
        password_hash VARCHAR(100),
        user_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES managers (id) ON DELETE CASCADE
    """
)

user_session = (
    """
        id SERIAL PRIMARY KEY,
        session VARCHAR(256),
        logined TIMESTAMP DEFAULT now(),
        user_id INTEGER,
        is_active BOOLEAN DEFAULT TRUE,
        FOREIGN KEY (user_id) REFERENCES managers (id) ON DELETE CASCADE
    """
)

customers = (
    """
        id SERIAL PRIMARY KEY,
        name VARCHAR(50),
        email VARCHAR(50),
        dt_reg DATE,
        manag_id INTEGER,
        sex CHAR(1),
        FOREIGN KEY (manag_id) REFERENCES managers (id) ON DELETE CASCADE
    """
)

office_heads = (
    """
        id SERIAL PRIMARY KEY,
        office_id INTEGER,
        manag_id INTEGER,
        FOREIGN KEY (office_id) REFERENCES offices (id) ON DELETE CASCADE,
        FOREIGN KEY (manag_id) REFERENCES managers (id) ON DELETE CASCADE
    """
)

products = (
    """
        id SERIAL PRIMARY KEY,
        name VARCHAR(30),
        category VARCHAR(15),
        price NUMERIC
    """
)

reviews = (
    """
        dt_rep DATE,
        cust_id INTEGER,
        manag_id INTEGER,
        result INTEGER,
        FOREIGN KEY (manag_id) REFERENCES managers (id) ON DELETE CASCADE,
        FOREIGN KEY (cust_id) REFERENCES customers (id) ON DELETE CASCADE
    """
)

plans = (
    """
    dt_rep DATE,
    manag_id INTEGER,
    office_id INTEGER,
    category VARCHAR(50),
    plan NUMERIC,
    FOREIGN KEY (manag_id) REFERENCES managers (id) ON DELETE CASCADE,
    FOREIGN KEY (office_id) REFERENCES offices (id) ON DELETE CASCADE
    """
)

sales = (
    """
        id SERIAL PRIMARY KEY,
        dt_rep DATE,
        cust_id INTEGER,
        office_id INTEGER,
        manag_id INTEGER,
        prod_id INTEGER,
        amount NUMERIC,
        cnt NUMERIC,
        FOREIGN KEY (cust_id) REFERENCES customers (id) ON DELETE CASCADE,
        FOREIGN KEY (office_id) REFERENCES offices (id) ON DELETE CASCADE,
        FOREIGN KEY (manag_id) REFERENCES managers (id) ON DELETE CASCADE,
        FOREIGN KEY (prod_id) REFERENCES products (id) ON DELETE CASCADE
    """
)