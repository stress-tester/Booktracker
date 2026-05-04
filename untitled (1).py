import tkinter as tk
from tkinter import messagebox
import requests
import json

# Файл для хранения избранных пользователей
FAVORITES_FILE = 'favorites.json'

# Загрузка избранных пользователей из JSON
def load_favorites():
    try:
        with open(FAVORITES_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

favorites = load_favorites()

# Поиск пользователя на GitHub
def search_user():
    username = entry.get()
    if not username:
        messagebox.showerror("Ошибка", "Поле поиска не должно быть пустым.")
        return

    response = requests.get(f"https://api.github.com/users/{username}")
    if response.status_code == 200:
        user_data = response.json()
        name = user_data.get('name', 'Не указано')
        user_info = f"{name} ({username})"
        listbox.insert(tk.END, user_info)
    else:
        messagebox.showerror("Ошибка", "Пользователь не найден.")

# Сохранение избранных пользователей в JSON
def save_favorites():
    with open(FAVORITES_FILE, 'w') as f:
        json.dump(favorites, f)

# Добавление пользователя в избранное
def add_to_favorites():
    if listbox.curselection():
        user = listbox.get(listbox.curselection())
        username = user.split('(')[-1].strip(' )')
        if username not in favorites:
            favorites.append(username)
            save_favorites()
            messagebox.showinfo("Успех", f"{username} добавлен в избранное!")
        else:
            messagebox.showwarning("Уже в избранном", f"{username} уже находится в избранных.")
    else:
        messagebox.showwarning("Предупреждение", "Выберите пользователя для добавления в избранное.")

# Создание основного окна
root = tk.Tk()
root.title("GitHub User Finder")

# Поле для ввода имени пользователя
entry = tk.Entry(root, width=50)
entry.pack(pady=10)

# Кнопка поиска
search_button = tk.Button(root, text="Поиск пользователя", command=search_user)
search_button.pack(pady=5)

# Список пользователей
listbox = tk.Listbox(root, width=50)
listbox.pack(pady=10)

# Кнопка добавления в избранное
favorite_button = tk.Button(root, text="Добавить в избранное", command=add_to_favorites)
favorite_button.pack(pady=5)

# Запуск основного цикла
root.mainloop()
