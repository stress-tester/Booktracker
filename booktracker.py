import tkinter as tk
from tkinter import messagebox, ttk
import json
from datetime import datetime

# Файл для хранения тренировок
TRAININGS_FILE = 'trainings.json'

# Загрузка тренировок из JSON
def load_trainings():
    try:
        with open(TRAININGS_FILE, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []

trainings = load_trainings()

# Сохранение тренировок в JSON
def save_trainings():
    with open(TRAININGS_FILE, 'w') as f:
        json.dump(trainings, f)

# Добавление тренировки
def add_training():
    date_str = date_entry.get()
    training_type = type_entry.get()
    duration_str = duration_entry.get()

    # Проверка корректности ввода
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        messagebox.showerror("Ошибка", "Дата должна быть в формате YYYY-MM-DD.")
        return

    try:
        duration = float(duration_str)
        if duration <= 0:
            raise ValueError
    except ValueError:
        messagebox.showerror("Ошибка", "Длительность должна быть положительным числом.")
        return

    training = {
        'date': date_str,
        'type': training_type,
        'duration': duration
    }
    trainings.append(training)
    save_trainings()
    load_trainings_to_table()
    clear_entries()

def clear_entries():
    date_entry.delete(0, tk.END)
    type_entry.delete(0, tk.END)
    duration_entry.delete(0, tk.END)

def load_trainings_to_table(filtered=None):
    for row in training_table.get_children():
        training_table.delete(row)

    for training in (filtered if filtered else trainings):
        training_table.insert('', 'end', values=(training['date'], training['type'], training['duration']))

def filter_trainings():
    filtered = []
    training_type = filter_type_entry.get()
    date_str = filter_date_entry.get()

    for training in trainings:
        if (not training_type or training['type'] == training_type) and \
           (not date_str or training['date'] == date_str):
            filtered.append(training)
    
    load_trainings_to_table(filtered)

# Основное окно
root = tk.Tk()
root.title("Training Planner")

# Секции для ввода тренировок
frame = tk.Frame(root)
frame.pack(pady=10)

tk.Label(frame, text="Дата (YYYY-MM-DD)").grid(row=0, column=0)
date_entry = tk.Entry(frame)
date_entry.grid(row=0, column=1)

tk.Label(frame, text="Тип тренировки").grid(row=1, column=0)
type_entry = tk.Entry(frame)
type_entry.grid(row=1, column=1)

tk.Label(frame, text="Длительность (в минутах)").grid(row=2, column=0)
duration_entry = tk.Entry(frame)
duration_entry.grid(row=2, column=1)

add_button = tk.Button(frame, text="Добавить тренировку", command=add_training)
add_button.grid(row=3, columnspan=2, pady=5)

# Секция для фильтрации
filter_frame = tk.Frame(root)
filter_frame.pack(pady=10)

tk.Label(filter_frame, text="Фильтр по типу").grid(row=0, column=0)
filter_type_entry = tk.Entry(filter_frame)
filter_type_entry.grid(row=0, column=1)

tk.Label(filter_frame, text="Фильтр по дате").grid(row=1, column=0)
filter_date_entry = tk.Entry(filter_frame)
filter_date_entry.grid(row=1, column=1)

filter_button = tk.Button(filter_frame, text="Применить фильтр", command=filter_trainings)
filter_button.grid(row=2, columnspan=2)

# Таблица для отображения тренировок
columns = ('Дата', 'Тип тренировки', 'Длительность')
training_table = ttk.Treeview(root, columns=columns, show='headings')
for col in columns:
    training_table.heading(col, text=col)
training_table.pack(pady=10)

load_trainings_to_table()

# Запуск основного цикла
root.mainloop()
