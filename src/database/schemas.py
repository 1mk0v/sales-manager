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
        session VARCHAR(50),
        logined TIMESTAMP,
        user_id INTEGER,
        is_active BOOLEAN DEFAULT TRUE,
        FOREIGN KEY (user_id) REFERENCES managers (id) ON DELETE CASCADE
    """
)