"""
Guia de estudos: Injeção de Dependências e Testes no FastAPI

Como funciona o `app.dependency_overrides`:
1. O FastAPI permite sobrescrever qualquer dependência definida com `Depends()`.
2. A sintaxe é:
       app.dependency_overrides[dependencia_original] = substituto
3. O `substituto` DEVE ser uma função/callable, pois o FastAPI a invoca para obter o valor.
4. Por isso usamos `lambda: repository`:
   - É uma função anônima que não recebe parâmetros e retorna a instância `repository`.
   - É equivalente a:
         def fake_get_task_repository():
             return repository
   - Passar apenas `repository` direto geraria erro, pois o objeto não é chamável (callable).
5. Isolamento dos testes:
   - Criar `repository = InMemoryTaskRepository()` dentro de cada teste garante que cada
     cenário use uma base limpa e sem efeitos colaterais de outros testes.
6. Limpeza (`finally`):
   - `app.dependency_overrides.clear()` remove as substituições, garantindo que os próximos
     testes não sejam afetados.
"""

from http import HTTPStatus

from app.db.dependencies import get_task_repository
from app.db.repository import InMemoryTaskRepository
from app.main import app
from app.models.tarefa import Tarefa

# def test_home(client):
#     # A - Arrange
#     response = client.get('/') # A - Act
#     assert response.status_code == HTTPStatus.OK # A - Assert
#     assert response.json() == {'mensagem': 'Hello, World!!!!'}


def test_criar_tarefa_usa_repositorio_injetado(client) -> None:
    repository = InMemoryTaskRepository()
    # Substitui a dependência por um repositório limpo e isolado para este teste:
    app.dependency_overrides[get_task_repository] = lambda: repository

    try:
        response = client.post(
            "/tarefas/",
            json={
                "titulo": "Aprender DI",
                "descricao": "Testar uma dependência substituível",
                "concluida": False,
                "tags": ["python"],
            },
        )

        assert response.status_code == HTTPStatus.CREATED
        resposta = response.json()
        assert resposta["id"] == 1
        assert resposta["titulo"] == "Aprender DI"
        assert resposta["descricao"] == "Testar uma dependência substituível"
        assert resposta["concluida"] is False
        assert resposta["tags"] == ["python"]
        assert "data_criacao" in resposta
        assert "data_atualizacao" in resposta
        assert len(repository.list()) == 1
    finally:
        app.dependency_overrides.clear()


def test_lista_tarefas_usa_repositorio_injetado(client) -> None:
    repository = InMemoryTaskRepository()
    # substitui a função por um repositório limpo exclusivo para este teste:
    app.dependency_overrides[get_task_repository] = lambda: repository
    repository.create(
        Tarefa(
            titulo="Tarefa teste",
            descricao="tarefa teste",
            concluida=True,
            tags=[],
        )
    )

    try:
        response = client.get("/tarefas/")

        assert response.status_code == HTTPStatus.OK
        resposta = response.json()
        assert len(resposta) == 1
        assert resposta[0]["id"] == 1
        assert resposta[0]["titulo"] == "Tarefa teste"
        assert len(repository.list()) == 1
    finally:
        app.dependency_overrides.clear()


def test_atualiza_tarefa_usa_repositorio_injetado(client) -> None:
    repository = InMemoryTaskRepository()
    # substitui a função por um repositório limpo exclusivo para este teste:
    app.dependency_overrides[get_task_repository] = lambda: repository
    tarefa_criada = repository.create(
        Tarefa(
            titulo="Aprender DI",
            descricao="Testar uma dependência substituível",
            concluida=False,
            tags=["python"],
        )
    )

    try:
        response = client.put(
            f"/tarefas/{tarefa_criada.id}",
            json={
                "titulo": "Aprender DI Atualizado",
                "descricao": "Testar uma dependência substituível atualizada",
                "concluida": True,
                "tags": ["python", "fastapi"],
            },
        )

        assert response.status_code == HTTPStatus.OK
        resposta = response.json()
        assert resposta["id"] == tarefa_criada.id
        assert resposta["titulo"] == "Aprender DI Atualizado"
        assert resposta["descricao"] == "Testar uma dependência substituível atualizada"
        assert resposta["concluida"] is True
        assert resposta["tags"] == ["python", "fastapi"]
        assert len(repository.list()) == 1
    finally:
        app.dependency_overrides.clear()


def test_deleta_tarefa_usa_repositorio_injetado(client) -> None:
    repository = InMemoryTaskRepository()
    # substitui a função por um repositório limpo exclusivo para este teste:
    app.dependency_overrides[get_task_repository] = lambda: repository
    tarefa_criada = repository.create(
        Tarefa(
            titulo="Aprender DI",
            descricao="Testar uma dependência substituível",
            concluida=False,
            tags=["python"],
        )
    )

    try:
        response = client.delete(f"/tarefas/{tarefa_criada.id}")

        assert response.status_code == HTTPStatus.NO_CONTENT
        assert len(repository.list()) == 0
    finally:
        app.dependency_overrides.clear()


def test_atualiza_tarefa_inexistente_retorna_404(client) -> None:
    repository = InMemoryTaskRepository()
    # substitui a função por um repositório limpo exclusivo para este teste:
    app.dependency_overrides[get_task_repository] = lambda: repository

    try:
        response = client.put(
            "/tarefas/999",
            json={
                "titulo": "Aprender DI",
                "descricao": "Testar uma dependência substituível",
                "concluida": False,
                "tags": ["python"],
            },
        )

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"detail": "Tarefa não encontrada"}
    finally:
        app.dependency_overrides.clear()


def test_deleta_tarefa_inexistente_retorna_404(client) -> None:
    repository = InMemoryTaskRepository()
    # substitui a função por um repositório limpo exclusivo para este teste:
    app.dependency_overrides[get_task_repository] = lambda: repository

    try:
        response = client.delete("/tarefas/999")

        assert response.status_code == HTTPStatus.NOT_FOUND
        assert response.json() == {"detail": "Tarefa não encontrada"}
    finally:
        app.dependency_overrides.clear()
