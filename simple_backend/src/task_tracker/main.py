from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from TaskTracker2 import TaskTracker
from cloudflare import CloudflareAPI

API_KEY = "$2a$10$M8sdgnbD7n2WFIoXe79euOqBckd20wOo0xtAzS3bd8P6n6mKpCzie"  # Замените на ваш реальный API-ключ
BIN_ID = None  # Идентификатор бина, используемый для хранения задач
CLOUDFLARE_API_KEY = "56740052615052922baf774b5c38e428cdf79"  # Ваш API-ключ Cloudflare
CLOUDFLARE_EMAIL = "andrey211211@mail.ru"  # Ваш email для Cloudflare

app = FastAPI()

class Task(BaseModel):
    task_id: int
    task: str
    status: str
    suggestion: str = ""  # Поле для хранения фрагмента решения (по умолчанию пустое)

task_tracker = TaskTracker(API_KEY, BIN_ID)
cloudflare_api = CloudflareAPI(CLOUDFLARE_API_KEY, CLOUDFLARE_EMAIL)


@app.get("/tasks")
def get_tasks():
    return task_tracker.load_tasks()  # Получаем все задачи

@app.post("/tasks")
def create_task(task: Task):
    solution = cloudflare_api.generate_solution(task.task)
    if solution:
        task.suggestion = solution  # Сохраняем предложение в отдельном поле
    else:
        print("Не удалось сгенерировать решение с помощью Cloudflare API")
        #  Решить, что делать, если не удалось сгенерировать решение.
        #  Например, можно вернуть ошибку клиенту:
        # raise HTTPException(status_code=500, detail="Не удалось сгенерировать решение")

    task_tracker.add_task(task.model_dump())
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, task: Task):
    try:
        task_tracker.update_task(task_id, task.model_dump())  # Обновляем задачу
        return task
    except ValueError:
        raise HTTPException(status_code=404, detail="нет такого айди")

@app.delete("/tasks/{task_id}")
def delete_task(task_id: int):
    try:
        deleted_task = task_tracker.remove_task(task_id)  # Удаляем задачу
        return deleted_task
    except ValueError:
        raise HTTPException(status_code=404, detail="нет такого айди")
