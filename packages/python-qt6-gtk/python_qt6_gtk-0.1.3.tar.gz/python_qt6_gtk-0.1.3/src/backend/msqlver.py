import pyodbc
from backend.schema import OrderItem

class Database:
    def __init__(self, username: str, password: str) -> None:
        self.conn = Database.connect_to_db(username, password)
        if self.conn is None:
            raise Exception("Connection to the database failed.")
    
    @staticmethod
    def connect_to_db(username: str, password: str):
        """Подключение к Microsoft SQL Server"""
        try:
            conn = pyodbc.connect(
                f"DRIVER={{ODBC Driver 17 for SQL Server}};"
                f"SERVER=localhost;"
                f"DATABASE=cafe_project4;"
                f"UID={username};"
                f"PWD={password};"
                "Trusted_Connection=no;"
            )
            return conn
        except pyodbc.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    def query(self, query, params=None):
        """Общий метод для выполнения запросов"""
        cursor = self.conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conn.commit()
        except pyodbc.Error as err:
            print(f"Error: {err}")
        finally:
            cursor.close()

    # Admin functions
    def register_user(self, username: str, full_name: str, password: str, role: str) -> None:
        cursor = self.conn.cursor()
        try:
            # Добавление пользователя в таблицу users
            query = "INSERT INTO users (username, full_name, role) VALUES (?, ?, ?)"
            cursor.execute(query, (username, full_name, role))

            # Создание пользователя в Microsoft SQL Server
            query = f"CREATE LOGIN [{username}] WITH PASSWORD = '{password}';"
            cursor.execute(query)
            query = f"CREATE USER [{username}] FOR LOGIN [{username}];"
            cursor.execute(query)

            self.conn.commit()
            print(f"Пользователь {username} успешно зарегистрирован.")
        except pyodbc.Error as err:
            print(f"Error registering user: {err}")
        finally:
            cursor.close()

    def get_users(self):
        cursor = self.conn.cursor()
        try:
            query = "SELECT * FROM users"
            cursor.execute(query)
            users = cursor.fetchall()
            return users
        except pyodbc.Error as err:
            print(f"Error fetching users: {err}")
            return []
        finally:
            cursor.close()
    
    def fire_user(self, user_id: int):
        cursor = self.conn.cursor()
        try:
            query = "UPDATE users SET status = 'fired' WHERE id = ?"
            cursor.execute(query, (user_id,))
            self.conn.commit()
        except pyodbc.Error as err:
            print(f"Error firing user: {err}")
        finally:
            cursor.close()

    # Функции для работы со сменами
    def assign_shift(self, user_id: int, start_time, end_time) -> None:
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO shifts (user_id, start_time, end_time) VALUES (?, ?, ?)"
            cursor.execute(query, (user_id, start_time, end_time))
            self.conn.commit()
        except pyodbc.Error as err:
            print(f"Error assigning shift: {err}")
        finally:
            cursor.close()

    def create_order(self, waiter_id: int, table_id: int, items: list[OrderItem]):
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO orders (waiter_id, table_id) VALUES (?, ?)"
            cursor.execute(query, (waiter_id, table_id))
            order_id = cursor.execute("SELECT SCOPE_IDENTITY()").fetchone()[0]
            
            query = "INSERT INTO order_items (order_id, item_name, quantity, price) VALUES (?, ?, ?, ?)"
            for item in items:
                cursor.execute(query, (order_id, item.name, item.quantity, item.price))
            
            self.conn.commit()
        except pyodbc.Error as err:
            print(f"Error creating order: {err}")
        finally:
            cursor.close()

    def get_all_orders(self) -> list:
        cursor = self.conn.cursor()
        try:
            query = "SELECT * FROM orders"
            cursor.execute(query)
            orders = cursor.fetchall()
            return orders
        except pyodbc.Error as err:
            print(f"Error fetching orders: {err}")
            return []
        finally:
            cursor.close()
    
    def get_orders(self, status: str):
        cursor = self.conn.cursor()
        try:
            query = "SELECT * FROM orders WHERE status = ?"
            cursor.execute(query, (status,))
            orders = cursor.fetchall()
            return orders
        except pyodbc.Error as err:
            print(f"Error fetching orders by status: {err}")
            return []
        finally:
            cursor.close()

    def change_order_status(self, order_id, status: str):
        cursor = self.conn.cursor()
        try:
            query = "UPDATE orders SET status = ? WHERE id = ?"
            cursor.execute(query, (status, order_id))
            self.conn.commit()
        except pyodbc.Error as err:
            print(f"Error updating order status: {err}")
        finally:
            cursor.close()

    def create_table(self, capacity: int):
        cursor = self.conn.cursor()
        try:
            query = "INSERT INTO tables (capacity) VALUES (?)"
            cursor.execute(query, (capacity,))
            self.conn.commit()
        except pyodbc.Error as err:
            print(f"Error creating table: {err}")
        finally:
            cursor.close()

    def get_user_id_by_username(self, username: str) -> int:
        cursor = self.conn.cursor()
        try:
            query = "SELECT id FROM users WHERE username = ?"
            cursor.execute(query, (username,))
            result = cursor.fetchone()
            return result[0] if result else None
        except pyodbc.Error as err:
            print(f"Error getting user ID: {err}")
            return None
        finally:
            cursor.close()
