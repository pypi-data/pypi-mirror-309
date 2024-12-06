import mysql.connector
from mysql.connector.connection_cext import CMySQLConnection
from backend.schema import OrderItem

class Database:
    def __init__(self, username: str, password: str) -> None:
        self.conn = Database.connect_to_db(username, password)
        if self.conn is None:
            raise mysql.connector.Error
    
    @staticmethod
    def connect_to_db(username: str, password: str) -> CMySQLConnection:
        """todo"""
        try:
            return mysql.connector.connect(
                host='localhost',
                user=username,
                password=password,
                database='cafe_project4',
                charset="utf8mb4",
                collation="utf8mb4_general_ci"
            )
        except mysql.connector.Error:
            return None
    
    def query(self, query):
        """todo"""
        curson = self.conn.cursor()
        try:
            curson.execute(query)
        except mysql.connector.Error as err:
            print(f"Error: {err}")
            return 

        self.conn.commit()
    
    # Admin functions
    def register_user(self, username: str, full_name: str, password: str, role: str) -> None:
        """todo"""
        cursor = self.conn.cursor()
        
        query = "INSERT INTO users (username, full_name, role) VALUES (%s, %s, %s)"
        cursor.execute(query, (username, full_name, role))
        
        query = f"CREATE USER '{username}'@'localhost' IDENTIFIED BY '{password}'"
        cursor.execute(query)
                
        self.conn.commit()
        print(f"Пользователь {username} успешно зарегистрирован.")
    
    def get_users(self):
        cursor = self.conn.cursor()
        query = "SELECT * FROM users"
        cursor.execute(query)
        users = cursor.fetchall()
        return users
        
    def fire_user(self, user_id: int):
        """todo"""
        cursor = self.conn.cursor()
        query = "UPDATE users SET status = 'fired' WHERE id = %s"
        cursor.execute(query, (user_id,))
        self.conn.commit()
    
    # Функции для работы со сменами
    def assign_shift(self, user_id: int, start_time, end_time) -> None:
        """todo"""
        cursor = self.conn.cursor()
        query = "INSERT INTO shifts (user_id, start_time, end_time) VALUES (%s, %s, %s)"
        cursor.execute(query, (user_id, start_time, end_time))
        self.conn.commit()
    
    def create_order(self, waiter_id: int, table_id: int, items: list[OrderItem]):
        """todo"""
        cursor = self.conn.cursor()
        query = "INSERT INTO orders (waiter_id, table_id) VALUES (%s, %s)"
        cursor.execute(query, (waiter_id, table_id))
        
        order_id = cursor.lastrowid
        query = "INSERT INTO order_items (order_id, item_name, quantity, price) VALUES (%s, %s, %s, %s)"
        for item in items:
            cursor.execute(query, (order_id, item.name, item.quantity, item.price))
        
        self.conn.commit()
    
    def get_all_orders(self) -> list:
        """todo"""
        cursor = self.conn.cursor()
        query = "SELECT * FROM orders"
        cursor.execute(query)
        orders = cursor.fetchall()
        return orders
    
    def get_orders(self, status: str):
        """todo"""
        cursor = self.conn.cursor()
        query = "SELECT * FROM orders WHERE status = %s"
        cursor.execute(query, (status,))
        orders = cursor.fetchall()
        return orders
    
    def change_order_status(self, order_id, status: str):
        """todo"""
        cursor = self.conn.cursor()
        query = "UPDATE orders SET status = %s WHERE id = %s"
        cursor.execute(query, (order_id, status))
        self.conn.commit()
        
    def create_table(self, capacity: int):
        """todo"""
        cursor = self.conn.cursor()
        query = "INSERT INTO tables (capacity) VALUES (%s)"
        cursor.execute(query, (capacity,))
        self.conn.commit()
        
    def get_user_id_by_username(self, username: str) -> int:
        """Получает ID пользователя по его имени."""
        cursor = self.conn.cursor()
        query = "SELECT id FROM users WHERE username = %s"
        cursor.execute(query, (username,))
        result = cursor.fetchone()
        if result:
            return result[0]
        else:
            return None 