from datetime import datetime

from sqlalchemy import JSON, func
from sqlalchemy.orm import Mapped, mapped_as_dataclass, mapped_column, registry

table_registry = registry()


@mapped_as_dataclass(table_registry)
class TarefaORM:
    __tablename__ = "tarefas"

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    titulo: Mapped[str]
    descricao: Mapped[str]
    concluida: Mapped[bool] = mapped_column(default=False)
    tags: Mapped[list[str]] = mapped_column(JSON, default_factory=list)
    data_criacao: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    data_atualizacao: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )
