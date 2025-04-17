import json

class TaskTracker:
    def __init__(self, file_path):
        self.file_path = file_path
        self.tasks = self.load_tasks()  # Загружаем задачи при инициализации

    def load_tasks(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)  # Возвращаем список задач
        except FileNotFoundError:
            return []  # Возвращаем пустой список, если файл не найден

    def save_tasks(self):
        with open(self.file_path, "w") as f:
            json.dump(self.tasks, f)  # Сохраняем задачи с отступами

    def add_task(self, task):
        self.tasks.append(task)  # Добавляем новую задачу в список
        self.save_tasks()  # Сохраняем изменения

    def update_task(self, task_id: int, updated_task):
        for i, task in enumerate(self.tasks):
            if task["task_id"] == task_id:
                self.tasks[i] = updated_task  # Обновляем задачу
                self.save_tasks()  # Сохраняем изменения
                return  # Завершаем в случае успеха
        raise ValueError("Нет такой задачи с данным ID")  # Если задача не найдена

    def remove_task(self, task_id: int):
        for i, task in enumerate(self.tasks):
            if task["task_id"] == task_id:
                deleted_task = self.tasks.pop(i)  # Удаляем задачу
                self.save_tasks()  # Сохраняем изменения после удаления
                return deleted_task
        raise ValueError("Нет такой задачи с данным ID")
