from sqlalchemy import select

from app.models.tarefa_orm import TarefaORM


def test_criar_tarefa_no_banco(session):
    tarefa = TarefaORM(
        titulo="Estudar SQLAlchemy",
        descricao="Aprender mapeamento ORM com dataclass",
        concluida=False,
        tags=["python", "sqlalchemy"],
    )
    session.add(tarefa)
    session.commit()

    tarefa_bd = session.scalar(
        select(TarefaORM).where(TarefaORM.titulo == "Estudar SQLAlchemy")
    )

    assert tarefa_bd is not None
    assert tarefa_bd.id == 1
    assert tarefa_bd.titulo == "Estudar SQLAlchemy"
    assert tarefa_bd.concluida is False
    assert tarefa_bd.tags == ["python", "sqlalchemy"]
    assert tarefa_bd.data_criacao is not None
    assert tarefa_bd.data_atualizacao is not None
