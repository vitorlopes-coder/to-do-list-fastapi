from fastapi import FastAPI

from routers.tarefa_route import router as tarefa_router

app = FastAPI()

app.include_router(tarefa_router, prefix="/tarefas", tags=["Tarefas"])


@app.get("/")
def root():
    return {"mensage": "Olá Mundo"}
