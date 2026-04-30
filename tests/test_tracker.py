import pytest
from pytestqt.qtbot import QtBot
from PyQt5 import QtWidgets # или PySide6, в зависимости от того, что использует tkinter (здесь пример для PyQt, но логика та же)
import sys
import os
import json

# Импортируем основной класс приложения.
# ВАЖНО: Ваш main.py должен быть изменен так, чтобы класс TaskApp был доступен для импорта.
# См. раздел "Изменение main.py" ниже.
from main import TaskApp

# --- Конфигурация тестов ---
HISTORY_FILE = "task_history.json"

@pytest.fixture(autouse=True)
def cleanup_history_file():
    """Фикстура: удаляет файл истории перед каждым тестом, чтобы они не влияли друг на друга."""
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)
    yield
    # Также удаляем после теста
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

def test_default_tasks_loaded(qtbot):
    """Проверка: предопределенные задачи загружаются при старте."""
    app = TaskApp(None) # None вместо root, так как мы не запускаем цикл mainloop
    assert "Учёба" in app.all_tasks
    assert "Прочитать статью" in app.all_tasks["Учёба"]
    assert "Спорт" in app.all_tasks
    assert "Сделать зарядку" in app.all_tasks["Спорт"]

def test_generate_task_updates_label(qtbot):
    """Проверка: при генерации задача отображается в главном лейбле."""
    app = TaskApp(None)
    initial_text = app.task_label.cget("text")
    
    # Вызываем метод генерации напрямую
    app.generate_task()
    
    new_text = app.task_label.cget("text")
    assert new_text != initial_text, "Текст лейбла не изменился после генерации"
    assert "Задача:" in new_text

def test_history_saved_to_file(qtbot):
    """Проверка: сгенерированная задача сохраняется в файл JSON."""
    app = TaskApp(None)
    
    # Генерируем задачу
    app.generate_task()
    
    # Проверяем, что файл создался и он не пустой
    assert os.path.exists(HISTORY_FILE), "Файл истории не был создан"
    
    with open(HISTORY_FILE, "r") as f:
        data = json.load(f)
        assert len(data) == 1, "В файле истории должно быть 1 задание"

def test_add_custom_task_success(qtbot):
    """Проверка: новая задача успешно добавляется в список."""
    app = TaskApp(None)
    
    # Устанавливаем значения в виджеты
    app.new_task_entry.delete(0, 'end')
    app.new_task_entry.insert(0, "Тестовая задача")
    app.type_var.set("Учёба")
    
    # Вызываем метод добавления
    app.add_custom_task()
    
    # Проверяем, что задача добавлена в список
    assert "Тестовая задача" in app.all_tasks["Учёба"]

def test_add_custom_task_empty_string(qtbot, mocker):
    """Проверка: попытка добавить пустую строку выводит ошибку."""
    app = TaskApp(None)
    
    # Подменяем messagebox.showerror, чтобы тест не зависал на окне
    mock_showerror = mocker.patch('tkinter.messagebox.showerror')
    
    # Пробуем добавить пустую задачу
    app.new_task_entry.delete(0, 'end') # Очищаем поле
    app.type_var.set("Спорт")
    
    app.add_custom_task()
    
    # Проверяем, что функция ошибки была вызвана с правильным сообщением
    mock_showerror.assert_called_once_with("Ошибка", "Поле задачи не может быть пустым!")
