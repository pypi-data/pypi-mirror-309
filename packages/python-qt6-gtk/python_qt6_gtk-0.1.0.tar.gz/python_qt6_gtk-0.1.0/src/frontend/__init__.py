import tkinter as tk
from tkinter import ttk, messagebox
from backend import Database

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
        
    tk.Button(login, text="Войти", command=login_check).grid(row=2, column=1)
    login.mainloop()
