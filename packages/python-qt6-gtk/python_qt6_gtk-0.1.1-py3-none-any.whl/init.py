from backend import Database 

conn = Database.connect_to_db("root", "root")
cursor = conn.cursor()

# Разделяем SQL-запросы
QUERIES = [
    "CREATE DATABASE cafe_project4;",
    "USE cafe_project4;",
    """
    CREATE TABLE users (
        id INT AUTO_INCREMENT PRIMARY KEY,
        username VARCHAR(50) UNIQUE NOT NULL,
        full_name VARCHAR(255) NOT NULL,
        role ENUM('admin', 'chef', 'waiter'),
        status ENUM('active', 'fired') DEFAULT 'active'
    );
    """,
    """
    CREATE TABLE tables (
        id INT AUTO_INCREMENT PRIMARY KEY,
        capacity INT
    );
    """,
    """
    CREATE TABLE orders (
        id INT AUTO_INCREMENT PRIMARY KEY,
        waiter_id INT,
        table_id INT,
        client_quantity INT,
        status ENUM('accepted', 'ready', 'paid') DEFAULT 'accepted',
        created_at DATETIME DEFAULT NOW(),
        updated_at DATETIME DEFAULT NOW(),
        FOREIGN KEY (waiter_id) REFERENCES users(id),
        FOREIGN KEY (table_id) REFERENCES tables(id)
    );
    """,
    """
    CREATE TABLE order_items (
        id INT AUTO_INCREMENT PRIMARY KEY,
        order_id INT,
        item_name VARCHAR(100),
        quantity INT,
        price DECIMAL(10, 2),
        FOREIGN KEY (order_id) REFERENCES orders(id)
    );
    """,
    # "CREATE ROLE 'admin';",
    # "CREATE ROLE 'waiter';",
    # "CREATE ROLE 'chef';",
    # "GRANT ALL PRIVILEGES ON cafe_project3.* TO 'admin';",
    # "GRANT SELECT, INSERT, UPDATE ON cafe_project3.orders TO 'waiter';",
    # "GRANT SELECT, INSERT, UPDATE ON cafe_project3.order_items TO 'waiter';",
    # "GRANT SELECT, UPDATE ON cafe_project3.orders TO 'chef';",
    # "FLUSH PRIVILEGES;"
]

# Выполняем каждый запрос отдельно
for query in QUERIES:
    try:
        print(query)
        # cursor.execute(query)
        # print(f"Executed: {query}")  # Для отладки, можно убрать
    except Exception as e:
        print(f"Error executing query: {query}")
        print(e)

conn.commit()