import tkinter as tk
from tkinter import ttk, messagebox
from backend import Database
from backend.schema import OrderItem
from datetime import datetime

def login_window():
    login = tk.Tk()
    login.title("Вход в систему")

    tk.Label(login, text="Имя пользователя:").grid(row=0, column=0)
    username_entry = tk.Entry(login)
    username_entry.grid(row=0, column=1)

    tk.Label(login, text="Пароль:").grid(row=1, column=0)
    password_entry = tk.Entry(login, show="*")
    password_entry.grid(row=1, column=1)

    def login_check():
        username = username_entry.get()
        password = password_entry.get()        
        conn = Database.connect_to_db(username, password)            

        if conn is None:
            messagebox.showerror("Ошибка", "Неверное имя пользователя или пароль")
            return
        else:
            login.destroy()  # Закрываем окно входа
            # user_role = get_user_role(username, Database(username, password))
            create_dashboard()

    tk.Button(login, text="Войти", command=login_check).grid(row=2, column=1)
    login.mainloop()


def create_order_window(parent):
    order_window = tk.Toplevel(parent)
    order_window.title("Create Order")

    tk.Label(order_window, text="Item Name").grid(row=0, column=0, padx=5, pady=5, sticky="w")
    item_name_entry = tk.Entry(order_window)
    item_name_entry.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(order_window, text="Customer").grid(row=1, column=0, padx=5, pady=5, sticky="w")
    customer_entry = tk.Entry(order_window)
    customer_entry.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(order_window, text="Address").grid(row=1, column=2, padx=5, pady=5, sticky="w")
    address_entry = tk.Entry(order_window)
    address_entry.grid(row=1, column=3, padx=5, pady=5)

    tk.Label(order_window, text="Status").grid(row=2, column=0, padx=5, pady=5, sticky="w")
    status_var = tk.StringVar(value="Confirmed")
    tk.Radiobutton(order_window, text="Confirmed", variable=status_var, value="Confirmed").grid(row=2, column=1, padx=5, pady=5, sticky="w")
    tk.Radiobutton(order_window, text="Pending", variable=status_var, value="Pending").grid(row=3, column=1, padx=5, pady=5, sticky="w")
    tk.Radiobutton(order_window, text="Cancelled", variable=status_var, value="Cancelled").grid(row=4, column=1, padx=5, pady=5, sticky="w")

    tk.Label(order_window, text="Description").grid(row=2, column=2, padx=5, pady=5, sticky="w")
    description_text = tk.Text(order_window, width=30, height=5)
    description_text.grid(row=2, column=3, rowspan=3, padx=5, pady=5)

    tk.Label(order_window, text="Quantity").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    quantity = tk.IntVar(value=1)
    tk.Button(order_window, text="-", command=lambda: quantity.set(max(1, quantity.get() - 1))).grid(row=5, column=1, padx=5, pady=5, sticky="w")
    tk.Label(order_window, textvariable=quantity).grid(row=5, column=1, padx=5, pady=5)
    tk.Button(order_window, text="+", command=lambda: quantity.set(quantity.get() + 1)).grid(row=5, column=1, padx=40, pady=5, sticky="w")

    tk.Button(order_window, text="Back", command=order_window.destroy).grid(row=6, column=0, columnspan=2, padx=5, pady=5)
    tk.Button(order_window, text="Create", command=lambda: print_order_data(item_name_entry, customer_entry, address_entry, status_var, description_text, quantity)).grid(row=6, column=2, columnspan=2, padx=5, pady=5)

def print_order_data(item_name, customer, address, status, description, quantity):
    print("Item Name:", item_name.get())
    print("Customer:", customer.get())
    print("Address:", address.get())
    print("Status:", status.get())
    print("Description:", description.get("1.0", tk.END))
    print("Quantity:", quantity.get())

def create_dashboard():
    root = tk.Tk()
    root.title("Orders Dashboard")

    # Верхняя панель
    top_frame = tk.Frame(root, bg="#E0E0E0")
    top_frame.pack(fill=tk.X)
    tk.Label(top_frame, text="Orders", font=("Arial", 16), bg="#E0E0E0").pack(side=tk.LEFT, padx=20, pady=10)
    tk.Button(top_frame, text="+ New Order", bg="#4CAF50", fg="white", command=lambda: create_order_window(root)).pack(side=tk.RIGHT, padx=20, pady=10)

    # Боковая панель (зеленого цвета)
    left_frame = tk.Frame(root, width=150, bg="#66BB6A")  # Зеленый фон
    left_frame.pack(side=tk.LEFT, fill=tk.Y)

    tk.Label(left_frame, text="Logo", bg="#66BB6A", pady=20).pack()

    tk.Button(left_frame, text="Dashboard", width=15).pack(pady=5)
    tk.Button(left_frame, text="Orders", width=15).pack(pady=5)
    tk.Button(left_frame, text="Returns", width=15).pack(pady=5)
    tk.Button(left_frame, text="Settings", width=15).pack(pady=5)
    tk.Button(left_frame, text="Account", width=15).pack(pady=20)

    # Основное содержимое
    main_frame = tk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Блоки с информацией о заказах
    info_frame = tk.Frame(main_frame)
    info_frame.pack(pady=20)
    
    def create_info_block(frame, title, value, color):
        block = tk.Frame(frame, borderwidth=2, relief="solid")
        block.pack(side=tk.LEFT, padx=10)
        tk.Label(block, text=title, bg=color, width=10, fg="white").pack()
        tk.Label(block, text=value, width=10).pack()

    create_info_block(info_frame, "Orders", "123", "#4285F4")  # Синий
    create_info_block(info_frame, "Shipping", "91", "#66BB6A")  # Зеленый
    create_info_block(info_frame, "Delivered", "23", "#7986CB") # Фиолетовый

    # Выпадающие списки и поле поиска (упрощенно)
    filter_frame = tk.Frame(main_frame)
    filter_frame.pack(pady=10)
    sort_combo = ttk.Combobox(filter_frame, values=["Most Recent Order", "Oldest Order"])
    sort_combo.pack(side=tk.LEFT, padx=5)
    sort_combo.current(0)
    status_combo = ttk.Combobox(filter_frame, values=["Packing", "Shipped", "Delivered"])
    status_combo.pack(side=tk.LEFT, padx=5)
    status_combo.current(0)
    tk.Entry(filter_frame).pack(side=tk.LEFT, padx=5)

    # Таблица заказов с использованием ttk.Treeview
    table_frame = tk.Frame(main_frame)
    table_frame.pack(fill=tk.BOTH, expand=True)

    tree = ttk.Treeview(table_frame, columns=("OrderID", "ItemName", "Customer", "Address", "Status", "Quantity"), show="headings")
    tree.heading("OrderID", text="Order ID")
    tree.heading("ItemName", text="Item Name")
    tree.heading("Customer", text="Customer")
    tree.heading("Address", text="Address")
    tree.heading("Status", text="Status")
    tree.heading("Quantity", text="Quantity")

    data = [
        ("3833", "Smartphone", "Alice", "123 Main St", "Confirmed", "8"),
        ("6432", "Laptop", "Bob", "456 Elm St", "Packing", "5"),
        ("2180", "Tablet", "Crystal", "789 Oak St", "Delivered", "1"),
        ("5438", "Headphones", "John", "101 Pine St", "Confirmed", "9"),
        ("9144", "Camera", "David", "202 Cedar St", "Processing", "2"),
        ("7689", "Printer", "Alice", "303 Maple St", "Cancelled", "2"),
        ("1323", "Smartwatch", "Crystal", "404 Birch St", "Shipping", "6"),
        ("7391", "Keyboard", "John", "505 Redwood St", "Cancelled", "10"),
        ("4915", "Monitor", "Alice", "606 Fir St", "Shipping", "6"),
        ("5548", "External Hard Drive", "David", "707 Oak St", "Delivered", "10"),
        ("5485", "Table Lamp", "Crystal", "808 Pine St", "Confirmed", "4"),
    ]

    for item in data:
        tree.insert("", tk.END, values=item)

    tree.pack(fill=tk.BOTH, expand=True)

    root.mainloop()
