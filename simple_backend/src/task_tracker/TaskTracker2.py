import requests

class TaskTracker:


    def __init__(self, api_key, bin_id):
        self.api_key = api_key  # Сохраняем ваш API-ключ
        self.bin_id = bin_id  # Идентификатор бина
        self.tasks = self.load_tasks()  # Загружаем задачи при инициализации

    def load_tasks(self):
        if self.bin_id is None:
            # Создаём новый бин, если его нет
            url = "https://api.jsonbin.io/v3/b"
            headers = {"X-Master-Key": self.api_key}
            response = requests.post(url, headers=headers, json={"record": []})
            self.bin_id = response.json()["metadata"]["id"]  # Сохраняем ID нового бина
            return []  # Возвращаем пустой список задач

        # Загружаем задачи из существующего бина
        url = f"https://api.jsonbin.io/v3/b/{self.bin_id}"
        headers = {"X-Master-Key": self.api_key}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()["record"]  # Возвращаем список задач
        return []  # Возвращаем пустой список в случае ошибки

    def save_tasks(self):
        url = f"https://api.jsonbin.io/v3/b/{self.bin_id}"  # URL для обновления бина
        headers = {"X-Master-Key": self.api_key}
        data = {"record": self.tasks}  # Наши задачи в формате JSON
        requests.put(url, headers=headers, json=data)  # Сохраняем задачи

    def add_task(self, task):
        self.tasks.append(task)  # Добавляем новую задачу
        self.save_tasks()  # Сохраняем изменения

    def update_task(self, task_id: int, updated_task):
        for i, task in enumerate(self.tasks):
            if task["task_id"] == task_id:  # Если задача найдена
                self.tasks[i] = updated_task  # Обновляем задачу
                self.save_tasks()  # Сохраняем изменения
                return
        raise ValueError("Нет такой задачи с данным ID")  # Если задача не найдена

    def remove_task(self, task_id: int):
        for i, task in enumerate(self.tasks):
            if task["task_id"] == task_id:  # Если задача найдена
                deleted_task = self.tasks.pop(i)  # Удаляем ее
                self.save_tasks()  # Сохраняем изменения
                return deleted_task
        raise ValueError("Нет такой задачи с данным ID")  # Если задача не найдена
