import tkinter as tk
from tkinter import ttk, messagebox
import random
import json
import os

# --- Конфигурация ---
HISTORY_FILE = "task_history.json"
DEFAULT_TASKS = {
    "Учёба": ["Прочитать статью", "Решить 10 задач", "Посмотреть лекцию", "Выучить 20 слов"],
    "Спорт": ["Сделать зарядку", "Пробежать 2 км", "100 приседаний", "Растяжка 15 минут"],
    "Работа": ["Написать отчет", "Провести созвон", "Разобрать почту", "Составить план на день"]
}

# --- Работа с историей ---
def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_history(history):
    with open(HISTORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, ensure_ascii=False, indent=2)

# --- Основная логика приложения ---
class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных задач")
        self.root.geometry("500x500")
        
        self.history = load_history()
        self.all_tasks = DEFAULT_TASKS.copy()
        
        self.create_widgets()
        self.update_history_display()

    def create_widgets(self):
        # Фильтр по типу задачи
        frame_filter = tk.Frame(self.root)
        frame_filter.pack(pady=5, fill=tk.X)
        
        tk.Label(frame_filter, text="Фильтр по типу:").pack(side=tk.LEFT)
        self.filter_var = tk.StringVar(value="Все")
        filter_options = ["Все"] + list(self.all_tasks.keys())
        ttk.Combobox(frame_filter, textvariable=self.filter_var, 
                    values=filter_options, state="readonly").pack(side=tk.LEFT, padx=5)
        
        # Кнопка генерации
        tk.Button(self.root, text="Сгенерировать задачу", 
                 command=self.generate_task, bg="#4CAF50", fg="white").pack(pady=10)
        
        # Поле вывода задачи
        self.task_label = tk.Label(self.root, text="Ваша задача появится здесь",
                                  font=("Arial", 14), wraplength=450)
        self.task_label.pack(pady=10)
        
        # Блок добавления новой задачи
        add_frame = tk.Frame(self.root)
        add_frame.pack(pady=10, fill=tk.X)
        
        tk.Label(add_frame, text="Новая задача:").pack(side=tk.LEFT)
        self.new_task_entry = tk.Entry(add_frame)
        self.new_task_entry.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        self.type_var = tk.StringVar(value="Учёба")
        ttk.Combobox(add_frame, textvariable=self.type_var, 
                    values=list(self.all_tasks.keys()), width=10, state="readonly").pack(side=tk.LEFT, padx=5)
        
        tk.Button(add_frame, text="Добавить в список", 
                 command=self.add_custom_task, bg="#2196F3", fg="white").pack(side=tk.LEFT)
        
        # История задач
        history_frame = tk.Frame(self.root)
        history_frame.pack(pady=10, fill=tk.BOTH, expand=True)
        
        tk.Label(history_frame, text="История сгенерированных задач:").pack(anchor="w")
        self.history_listbox = tk.Listbox(history_frame, height=8)
        self.history_listbox.pack(fill=tk.BOTH, expand=True)

    def generate_task(self):
        """Генерирует случайную задачу с учетом фильтра."""
        task_type = self.filter_var.get()
        
        if task_type == "Все":
            all_tasks_flat = [task for sublist in self.all_tasks.values() for task in sublist]
            if not all_tasks_flat:
                messagebox.showwarning("Нет задач", "Список задач пуст. Добавьте свои!")
                return
            task = random.choice(all_tasks_flat)
        else:
            if not self.all_tasks.get(task_type):
                messagebox.showwarning("Нет задач", f"В категории '{task_type}' нет задач.")
                return
            task = random.choice(self.all_tasks[task_type])
        
        self.task_label.config(text=f"Задача: {task}")
        
        # Сохранение в историю
        self.history.append(task)
        save_history(self.history)
        self.update_history_display()

    def update_history_display(self):
        """Обновляет виджет истории."""
        self.history_listbox.delete(0, tk.END)
        for task in self.history[-10:]:  # Показываем последние 10 задач
            self.history_listbox.insert(tk.END, task)

    def add_custom_task(self):
        """Добавляет новую задачу в список."""
        new_task_text = self.new_task_entry.get().strip()
        task_type = self.type_var.get()
        
        if not new_task_text:
            messagebox.showerror("Ошибка", "Поле задачи не может быть пустым!")
            return
            
        if task_type not in self.all_tasks:
            self.all_tasks[task_type] = []
            
        self.all_tasks[task_type].append(new_task_text)
        
        self.new_task_entry.delete(0, tk.END)
        messagebox.showinfo("Успех", f"Задача '{new_task_text}' добавлена в категорию '{task_type}'.")


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskApp(root)
    root.mainloop()
