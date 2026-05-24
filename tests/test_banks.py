# test_banks.py — testes do endpoint /api/banks/v1 da BrasilAPI
# Cada função que começa com test_ é reconhecida e executada pelo Pytest automaticamente

# "api_client" não é importado — o Pytest busca essa fixture no conftest.py sozinho


# Teste 1: verifica se a listagem de bancos retorna uma lista com itens
def test_listar_bancos_retorna_lista(api_client):
    # Arrange: nada a preparar, só precisamos do cliente

    # Act: faz a chamada GET /api/banks/v1
    response = api_client.get("/api/banks/v1")

    # Assert: verifica se o status foi 200 (sucesso) e se vieram itens
    assert response.status_code == 200        # a API respondeu com sucesso
    assert len(response.json()) > 0           # a lista não está vazia


# Teste 2: verifica se buscar um banco existente retorna os dados corretos
def test_buscar_banco_existente(api_client):
    # Arrange: vamos buscar o banco de código 1 (Banco do Brasil)
    codigo_banco = 1

    # Act: faz a chamada GET /api/banks/v1/1
    response = api_client.get(f"/api/banks/v1/{codigo_banco}")

    # Assert: verifica status 200 e se o código retornado bate com o que pedimos
    assert response.status_code == 200
    assert response.json()["code"] == codigo_banco    # "code" é o campo do código no JSON


# Teste 3: verifica se buscar um banco inexistente retorna 404
def test_banco_inexistente_retorna_404(api_client):
    # Arrange: código 99999 não existe na base de bancos
    codigo_invalido = 99999

    # Act: faz a chamada GET /api/banks/v1/99999
    response = api_client.get(f"/api/banks/v1/{codigo_invalido}")

    # Assert: a API deve informar que não encontrou (404 = Not Found)
    assert response.status_code == 404
