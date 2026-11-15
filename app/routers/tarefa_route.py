from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from app.db.dependencies import get_task_repository
from app.db.repository import TaskRepository
from app.models.tarefa import TarefaBD
from app.schemas.tarefa import Tarefa

router = APIRouter()
# Annotated: Guardando anotado ( variavel + metadado ) que esse tipo interface TaskRepository tem um metadado get_task_repository() instância que respeita seu contrato 
# Com isso evito multíplas instanciações 'repository: TaskRepository = Depends(get_task_repository)' em parâmetros para apenas TaskRepositoryDependency por
# parâmetro na rota
# Depends: injeção de dependência que chama uma função específica
# Vantagem nos testes: como a rota não está presa a uma instância fixa, nos testes você consegue usar app.dependency_overrides[get_task_repository] = lambda: repository para trocar o  
# repositório real por um repositório limpo em memória, sem alterar nada na rota.

TaskRepositoryDependency = Annotated[TaskRepository, Depends(get_task_repository)]


@router.get("/", response_model=list[TarefaBD])
def lista_tarefas(repository: TaskRepositoryDependency):
    return repository.list()


@router.post("/", response_model=TarefaBD, status_code=201)
def criar(tarefa: Tarefa, repository: TaskRepositoryDependency):
    return repository.create(tarefa)


@router.put("/{tarefa_id}", response_model=TarefaBD)
def atualizar(
    tarefa_id: int,
    tarefa: Tarefa,
    repository: TaskRepositoryDependency,
):
    tarefa_atualizada = repository.update(tarefa_id, tarefa)
    if tarefa_atualizada is None:
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")
    return tarefa_atualizada


@router.delete("/{tarefa_id}", status_code=204)
def excluir(tarefa_id: int, repository: TaskRepositoryDependency):
    if not repository.delete(tarefa_id):
        raise HTTPException(status_code=404, detail="Tarefa não encontrada")