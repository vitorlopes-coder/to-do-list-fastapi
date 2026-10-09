from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException

from db.dependencies import get_task_repository
from db.repository import TaskRepository
from models.tarefa import Tarefa
from schemas.tarefa import TarefaBD

router = APIRouter()
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