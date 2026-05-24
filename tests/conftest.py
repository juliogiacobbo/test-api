# conftest.py — configurações e fixtures compartilhadas entre todos os testes
# O Pytest encontra este arquivo automaticamente, sem precisar importar

import httpx                      # biblioteca que faz as chamadas HTTP
import pytest                     # framework de testes
from dotenv import load_dotenv    # lê o arquivo .env
import os                         # acessa variáveis de ambiente do sistema

# Lê o arquivo .env e carrega as variáveis na memória do programa
load_dotenv()

# Pega o valor de BASE_URL definido no .env
# Ex: "https://jsonplaceholder.typicode.com"
BASE_URL = os.getenv("BASE_URL")


# @pytest.fixture indica que esta função é uma preparação, não um teste
# O Pytest injeta automaticamente o cliente em qualquer teste que pedir "api_client"
@pytest.fixture
def api_client():
    # "with" garante que a conexão será fechada automaticamente ao final do teste
    with httpx.Client(base_url=BASE_URL) as client:
        yield client    # entrega o cliente pronto para o teste usar
