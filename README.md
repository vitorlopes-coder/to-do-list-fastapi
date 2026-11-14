# To-Do List API

API REST para gerenciamento de tarefas desenvolvida em **FastAPI** e gerenciada com o **uv**.

---

## 🚀 Requisitos

- [Python](https://www.python.org/) >= 3.14
- [uv](https://docs.astral.sh/uv/) (gerenciador de dependências e ambientes virtuais)

---

## 📦 Instalação

Clone o repositório e instale as dependências com o `uv`:

```bash
uv sync
```

---

## ▶️ Como Executar

### Modo Desenvolvimento (com auto-reload)

Para iniciar o servidor FastAPI diretamente da raiz do projeto:

```bash
uv run fastapi dev
```

> **Alternativa com Uvicorn:**
> ```bash
> uv run uvicorn app.main:app --reload
> ```

---

## 🌐 Endpoints e Documentação

Com o servidor em execução:

- **API Base:** [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Documentação Interativa (Swagger UI):** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **Documentação Alternativa (ReDoc):** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🧪 Como Rodar os Testes

Para executar os testes com o `pytest`:

```bash
uv run pytest
```

---

## 💡 Usando o Ambiente Virtual Diretamente

Se preferir não usar o comando `uv run` a cada execução, você pode ativar o ambiente virtual:

```bash
# Linux/macOS
source .venv/bin/activate

# Iniciar o servidor
fastapi dev
# ou: uvicorn app.main:app --reload

# Executar testes
pytest
```
