from db.repository import InMemoryTaskRepository, TaskRepository


task_repository = InMemoryTaskRepository()


def get_task_repository() -> TaskRepository:
    return task_repository