from fastapi.testclient import TestClient

from db.dependencies import get_task_repository
from db.repository import InMemoryTaskRepository
from main import app


def test_criar_tarefa_usa_repositorio_injetado() -> None:
    repository = InMemoryTaskRepository()
    app.dependency_overrides[get_task_repository] = lambda: repository

    try:
        response = TestClient(app).post(
            "/tarefas/",
            json={
                "titulo": "Aprender DI",
                "descricao": "Testar uma dependência substituível",
                "concluida": False,
                "tags": ["python"],
            },
        )

        assert response.status_code == 201
        assert response.json()["id"] == 1
        assert len(repository.list()) == 1
    finally:
        app.dependency_overrides.clear()