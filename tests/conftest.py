"""
Guia de estudos: Fixtures e o arquivo conftest.py no Pytest

1. O que é o arquivo `conftest.py`?
   - É um arquivo com nome reservado pelo Pytest para configurações e compartilhamento de fixtures.
   - O Pytest descobre e carrega esse arquivo automaticamente antes de rodar os testes.

2. Por que as fixtures podem ser acessadas tão facilmente (sem `import`)?
   - **Descoberta Automática (Auto-discovery):** Qualquer fixture definida no `conftest.py`
     fica disponível globalmente para todos os arquivos de teste no mesmo diretório (e subdiretórios).
     Não é necessário fazer `from conftest import client`.
   - **Injeção de Dependências por Nome:** Quando uma função de teste declara um parâmetro
     com o mesmo nome de uma fixture (ex: `def test_algo(client):`), o Pytest procura
     a fixture com esse nome, executa a função decorada com `@pytest.fixture` e injeta
     o seu retorno diretamente no teste.

3. O que esta fixture faz?
   - Instancia o `TestClient(app)` da FastAPI, que simula requisições HTTP para a aplicação
     sem precisar subir um servidor real de rede.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Retorna uma instância do TestClient configurada com o app FastAPI."""
    return TestClient(app)


@pytest.fixture
def cliente(client):
    """Alias(apelido) em português para a fixture 'client'."""
    return client

