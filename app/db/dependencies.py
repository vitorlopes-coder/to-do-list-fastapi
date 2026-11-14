from app.db.repository import InMemoryTaskRepository, TaskRepository

task_repository = InMemoryTaskRepository()

# interface de instânciação para o FastAPI

def get_task_repository() -> TaskRepository:
    return task_repository

    