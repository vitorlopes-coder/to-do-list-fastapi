from app.schemas.tarefa import Tarefa

class TarefaBD(Tarefa):
    id: int
    data_criacao: str
    data_atualizacao: str
