# Automação de Testes de API REST

Projeto de testes automatizados para a [ServeRest](https://serverest.dev), escrito em Python com Pytest e httpx.

---

## Pré-requisitos

- [Python 3.11+](https://www.python.org/downloads/) instalado na máquina
- Git

Para verificar se o Python está instalado, rode no terminal:

```
py --version
```

---

## Como rodar o projeto

### 1. Clone o repositório

```
git clone <url-do-repositorio>
cd test-api
```

### 2. Instale as dependências

```
py -m pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

Copie o arquivo de exemplo:

```
cp .env.example .env
```

O arquivo `.env` já vem com o valor correto para a ServeRest. Não é necessário alterar nada.

### 4. Rode os testes

```
py -m pytest -v
```

---

## O que é testado

Os testes cobrem o endpoint `/usuarios` da ServeRest, com os quatro métodos HTTP:

| Teste | Método | O que verifica |
|-------|--------|---------------|
| `test_listar_usuarios` | GET | lista de usuários retorna status 200 e formato correto |
| `test_criar_usuario` | POST | criação de usuário retorna status 201 e mensagem de sucesso |
| `test_buscar_usuario_existente` | GET | busca por ID retorna o usuário correto |
| `test_atualizar_usuario` | PUT | atualização retorna mensagem de sucesso |
| `test_deletar_usuario` | DELETE | exclusão retorna mensagem de sucesso |

---

## Estrutura do projeto

```
test-api/
├── .github/
│   └── workflows/
│       └── tests.yml         # pipeline do GitHub Actions
├── tests/
│   ├── conftest.py           # fixture com o cliente HTTP compartilhado
│   └── test_usuarios.py      # testes do endpoint de usuários
├── .env.example              # modelo de variáveis de ambiente
├── .gitignore                # arquivos ignorados pelo Git
├── requirements.txt          # dependências do projeto
└── README.md                 # este arquivo
```

---

## Interpretando o resultado dos testes

```
tests/test_usuarios.py::test_listar_usuarios PASSED
tests/test_usuarios.py::test_criar_usuario PASSED
tests/test_usuarios.py::test_buscar_usuario_existente PASSED
tests/test_usuarios.py::test_atualizar_usuario PASSED
tests/test_usuarios.py::test_deletar_usuario PASSED

5 passed in 2.34s
```

- `PASSED` — teste passou, comportamento está correto
- `FAILED` — teste falhou, algo está errado
- `ERROR` — erro antes do teste rodar (problema na fixture ou import)

---

## Problemas comuns

| Erro | Causa | Solução |
|------|-------|---------|
| `ModuleNotFoundError: No module named 'httpx'` | Dependências não instaladas | Rode `py -m pip install -r requirements.txt` |
| `fixture 'api_client' not found` | `conftest.py` fora do lugar | Verifique se está dentro da pasta `tests/` |
| `ConnectionError` | Sem internet ou URL errada | Verifique o valor de `BASE_URL` no `.env` |
| `AssertionError` | Resposta diferente do esperado | Verifique o endpoint chamado no teste |
