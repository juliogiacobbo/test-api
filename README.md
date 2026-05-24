# Automação de Testes de API REST

Projeto de testes automatizados para a [BrasilAPI](https://brasilapi.com.br), escrito em Python com Pytest e httpx.

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

Copie o arquivo de exemplo e preencha com os valores reais:

```
cp .env.example .env
```

O arquivo `.env` já vem com o valor correto para a BrasilAPI. Não é necessário alterar nada.

### 4. Rode os testes

```
py -m pytest -v
```

---

## O que é testado

Os testes cobrem o endpoint `/api/banks/v1` da BrasilAPI:

| Teste | O que verifica |
|-------|---------------|
| `test_listar_bancos_retorna_lista` | GET /api/banks/v1 retorna lista não vazia com status 200 |
| `test_buscar_banco_existente` | GET /api/banks/v1/1 retorna o Banco do Brasil com status 200 |
| `test_banco_inexistente_retorna_404` | GET /api/banks/v1/99999 retorna status 404 |

---

## Estrutura do projeto

```
test-api/
├── tests/
│   ├── conftest.py       # fixture com o cliente HTTP compartilhado
│   └── test_banks.py     # testes do endpoint de bancos
├── .env.example          # modelo de variáveis de ambiente
├── .gitignore            # arquivos ignorados pelo Git
├── requirements.txt      # dependências do projeto
└── README.md             # este arquivo
```

---

## Interpretando o resultado dos testes

```
tests/test_banks.py::test_listar_bancos_retorna_lista PASSED
tests/test_banks.py::test_buscar_banco_existente PASSED
tests/test_banks.py::test_banco_inexistente_retorna_404 PASSED

3 passed in 1.23s
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
