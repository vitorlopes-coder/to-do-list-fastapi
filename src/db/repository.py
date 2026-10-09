from collections.abc import Sequence
from datetime import datetime
from typing import Protocol

from models.tarefa import Tarefa
from schemas.tarefa import TarefaBD


class TaskRepository(Protocol):
    def list(self) -> Sequence[TarefaBD]: ...

    def create(self, tarefa: Tarefa) -> TarefaBD: ...

    def update(self, tarefa_id: int, tarefa: Tarefa) -> TarefaBD | None: ...

    def delete(self, tarefa_id: int) -> bool: ...


class InMemoryTaskRepository:
    def __init__(self) -> None:
        self._tasks: dict[int, TarefaBD] = {}
        self._next_id = 1

    def list(self) -> Sequence[TarefaBD]:
        return list(self._tasks.values())

    def create(self, tarefa: Tarefa) -> TarefaBD:
        agora = datetime.now().isoformat()
        nova_tarefa = TarefaBD(
            id=self._next_id,
            data_criacao=agora,
            data_atualizacao=agora,
            **tarefa.model_dump(),
        )
        self._tasks[self._next_id] = nova_tarefa
        self._next_id += 1
        return nova_tarefa

    def update(self, tarefa_id: int, tarefa: Tarefa) -> TarefaBD | None:
        tarefa_atual = self._tasks.get(tarefa_id)
        if tarefa_atual is None:
            return None

        tarefa_atualizada = TarefaBD(
            id=tarefa_id,
            data_criacao=tarefa_atual.data_criacao,
            data_atualizacao=datetime.now().isoformat(),
            **tarefa.model_dump(),
        )
        self._tasks[tarefa_id] = tarefa_atualizada
        return tarefa_atualizada

    def delete(self, tarefa_id: int) -> bool:
        return self._tasks.pop(tarefa_id, None) is not None