# test_usuarios.py — testes do endpoint /usuarios da ServeRest
# Cobre os quatro métodos HTTP: GET, POST, PUT e DELETE

import uuid    # gera identificadores únicos — usado para criar emails sem repetição


# Função auxiliar que cria um usuário e retorna os dados prontos
# Não é um teste (não começa com test_) — é um atalho usado pelos outros testes
def _novo_usuario():
    return {
        "nome": "Julio Teste",
        "email": f"julio_{uuid.uuid4()}@teste.com",   # email único a cada chamada
        "password": "senha123",
        "administrador": "true"
    }


# Teste 1: verifica se a listagem de usuários retorna os dados no formato esperado
def test_listar_usuarios(api_client):
    # Act
    response = api_client.get("/usuarios")

    # Assert
    assert response.status_code == 200
    assert "usuarios" in response.json()      # a resposta deve ter a chave "usuarios"
    assert isinstance(response.json()["usuarios"], list)   # e ela deve ser uma lista


# Teste 2: verifica se criar um usuário retorna status 201 e mensagem de sucesso
def test_criar_usuario(api_client):
    # Arrange
    usuario = _novo_usuario()

    # Act
    response = api_client.post("/usuarios", json=usuario)

    # Assert
    assert response.status_code == 201
    assert response.json()["message"] == "Cadastro realizado com sucesso"


# Teste 3: verifica se buscar um usuário existente retorna os dados corretos
def test_buscar_usuario_existente(api_client):
    # Arrange: cria um usuário para ter um ID válido para buscar
    criado = api_client.post("/usuarios", json=_novo_usuario())
    usuario_id = criado.json()["_id"]     # "_id" é o identificador gerado pela API

    # Act
    response = api_client.get(f"/usuarios/{usuario_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["_id"] == usuario_id    # confirma que veio o usuário certo


# Teste 4: verifica se atualizar um usuário retorna mensagem de sucesso
def test_atualizar_usuario(api_client):
    # Arrange: cria um usuário para depois atualizá-lo
    criado = api_client.post("/usuarios", json=_novo_usuario())
    usuario_id = criado.json()["_id"]

    dados_atualizados = {
        "nome": "Julio Atualizado",
        "email": f"julio_{uuid.uuid4()}@teste.com",   # novo email único
        "password": "senha456",
        "administrador": "false"
    }

    # Act
    response = api_client.put(f"/usuarios/{usuario_id}", json=dados_atualizados)

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Registro alterado com sucesso"


# Teste 5: verifica se deletar um usuário retorna mensagem de sucesso
def test_deletar_usuario(api_client):
    # Arrange: cria um usuário para depois deletá-lo
    criado = api_client.post("/usuarios", json=_novo_usuario())
    usuario_id = criado.json()["_id"]

    # Act
    response = api_client.delete(f"/usuarios/{usuario_id}")

    # Assert
    assert response.status_code == 200
    assert response.json()["message"] == "Registro excluído com sucesso"
