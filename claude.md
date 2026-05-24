# CLAUDE.md — Automação de Testes de API REST

## Como este guia funciona

Este projeto é construído passo a passo com foco em aprendizado.
Cada arquivo gerado vem acompanhado de uma explicação do que ele faz e por quê existe.
Não avançamos para o próximo passo até o atual estar funcionando e compreendido.

---

## Instruções para o Claude (leia antes de gerar qualquer arquivo)

Ao construir este projeto com o usuário:

1. **Explique antes de criar** — antes de gerar um arquivo, descreva em 2-3 linhas o que ele faz e por que ele precisa existir
2. **Explique o código gerado** — após criar um arquivo, destaque as linhas mais importantes e explique o raciocínio por trás delas
3. **Um passo de cada vez** — não gere múltiplos arquivos de uma vez; espere o usuário confirmar que entendeu antes de avançar
4. **Conecte os conceitos** — ao introduzir algo novo, diga como ele se relaciona com o que o usuário já viu
5. **Diga o que vai acontecer** — antes de rodar um comando, explique o que o usuário deve esperar ver na saída
6. **Normalize o erro** — quando algo falhar, explique que erros são parte do processo e ajude a interpretar a mensagem antes de corrigir
7. **Use comentários educativos** — todo código gerado deve ter comentários que explicam o "por quê", não apenas o "o quê"

---

## API usada neste projeto

**JSONPlaceholder** — `https://jsonplaceholder.typicode.com`

API pública, gratuita, sem cadastro e sem limite de uso. Perfeita para aprender.
Recursos disponíveis: `/posts`, `/users`, `/todos`, `/comments`.

Exemplos de chamadas que vamos testar:
- `GET /posts` → lista todos os posts
- `GET /posts/1` → busca o post de id 1
- `GET /posts/99999` → deve retornar 404 (não existe)

---

## Conceitos fundamentais (leia antes de ver o código)

### O que é um teste automatizado?
Um teste automatizado é um programa que verifica se outro programa se comporta como esperado.
Em vez de você abrir o Postman e verificar manualmente, o teste faz isso por você — sozinho, repetidamente, em qualquer ambiente.

### O que é Pytest?
Pytest é o framework que encontra, executa e reporta seus testes.
Qualquer função cujo nome começa com `test_` é automaticamente reconhecida como um teste.

### O que é uma fixture?
Uma fixture é uma função que prepara algo que os testes precisam.
Por exemplo: o cliente HTTP que conecta na API. Em vez de criar esse cliente em cada teste, você cria uma vez numa fixture e os testes recebem pronto.

### O que é conftest.py?
É o arquivo onde o Pytest procura fixtures automaticamente.
Você não precisa importar nada — o Pytest encontra sozinho qualquer fixture definida nesse arquivo.

### O que é httpx?
É a biblioteca que faz as chamadas HTTP (GET, POST, etc.) para a API.
Pense nela como um Postman programático — você escreve em Python o que faria manualmente no Postman.

### O que é o padrão AAA?
Arrange / Act / Assert — estrutura que deixa os testes legíveis:
- **Arrange**: prepara os dados de entrada
- **Act**: executa a ação (chama a API)
- **Assert**: verifica se o resultado está correto

---

## Stack

| Ferramenta | Para que serve |
|------------|----------------|
| Python 3.11+ | linguagem base |
| Pytest 7.x+ | roda e organiza os testes |
| httpx 0.27+ | faz chamadas HTTP na API |
| python-dotenv 1.x+ | carrega variáveis do arquivo `.env` |

---

## Estrutura de pastas

```
test-api/
├── .github/
│   └── workflows/
│       └── tests.yml        # instrui o GitHub Actions a rodar os testes
├── tests/
│   ├── conftest.py          # fixtures compartilhadas entre todos os testes
│   └── test_posts.py        # arquivo com os testes do recurso /posts
├── .env.example             # modelo de variáveis (esse vai pro git)
├── .env                     # variáveis reais locais (esse NÃO vai pro git)
├── .gitignore               # lista do que o git deve ignorar
├── requirements.txt         # lista as dependências do projeto
└── CLAUDE.md                # este arquivo
```

> Cada arquivo e pasta tem um propósito específico. Nada aqui é decoração.

---

## Ordem de construção (siga esta sequência)

A ordem importa para o aprendizado: cada etapa depende da anterior.

```
Passo 1 → requirements.txt        (diz quais bibliotecas instalar)
Passo 2 → .gitignore e .env       (protege arquivos sensíveis)
Passo 3 → tests/conftest.py       (cria o cliente HTTP compartilhado)
Passo 4 → tests/test_posts.py     (escreve os primeiros testes)
Passo 5 → rodar pytest -v         (ver os testes passando localmente)
Passo 6 → .github/workflows/tests.yml  (automatizar no GitHub Actions)
```

---

## Lendo o output do Pytest

Quando você rodar `pytest -v`, a saída vai parecer com isso:

```
tests/test_posts.py::test_buscar_post_existente PASSED    [ 33%]
tests/test_posts.py::test_listar_posts_retorna_lista PASSED    [ 66%]
tests/test_posts.py::test_post_inexistente_retorna_404 PASSED  [100%]

3 passed in 1.23s
```

- `PASSED` = teste passou, comportamento está correto
- `FAILED` = teste falhou, algo está errado
- `ERROR` = erro antes do teste rodar (geralmente um problema na fixture ou import)

Quando um teste falha, o Pytest mostra exatamente qual linha falhou e os valores envolvidos:

```
FAILED tests/test_posts.py::test_buscar_post_existente
AssertionError: assert 404 == 200
```

Isso significa: "esperávamos 200, mas recebemos 404." Ótima informação para depurar.

---

## Erros comuns e o que significam

| Erro | Causa provável | O que fazer |
|------|---------------|-------------|
| `ModuleNotFoundError: No module named 'httpx'` | biblioteca não instalada | rodar `pip install -r requirements.txt` |
| `fixture 'api_client' not found` | `conftest.py` não existe ou está no lugar errado | verificar se o arquivo está dentro da pasta `tests/` |
| `ConnectionError` | URL base errada ou sem internet | checar o valor de `BASE_URL` no `.env` |
| `AssertionError: assert 404 == 200` | endpoint errado ou dado não existe | revisar a URL chamada no teste |

---

## Rodando os testes localmente

```bash
# instalar as dependências (só precisa fazer uma vez)
pip install -r requirements.txt

# rodar todos os testes com saída detalhada
pytest -v

# rodar um único arquivo
pytest tests/test_posts.py -v

# rodar um único teste
pytest tests/test_posts.py::test_buscar_post_existente -v
```

---

## Pipeline GitHub Actions

Roda os testes de duas formas:
- **Manualmente**: clicando em "Run workflow" na aba Actions do repositório
- **Automaticamente**: todo dia às 8h UTC (5h horário de Brasília)

```yaml
# .github/workflows/tests.yml

name: Testes de API

on:
  workflow_dispatch:           # trigger manual pelo GitHub
  schedule:
    - cron: '0 8 * * *'       # todo dia às 8h UTC

jobs:
  testes:
    runs-on: ubuntu-latest     # roda numa máquina Linux temporária no GitHub

    steps:
      - name: Baixar o código
        uses: actions/checkout@v4          # copia o repositório para a máquina

      - name: Configurar Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'           # instala a versão do Python que usamos

      - name: Instalar dependências
        run: pip install -r requirements.txt   # instala httpx, pytest, etc.

      - name: Rodar os testes
        env:
          BASE_URL: ${{ vars.BASE_URL }}   # lê a variável configurada no GitHub
        run: pytest -v
```

Para configurar `BASE_URL` no GitHub:
1. Vá em **Settings → Secrets and variables → Actions → Variables**
2. Crie `BASE_URL` com valor `https://jsonplaceholder.typicode.com`

---

## Próximos passos (fase 2 — após dominar o básico)

Só avance quando os testes da fase 1 estiverem funcionando e você entender o que cada linha faz.

- **Markers** (`@pytest.mark.smoke`): categorizar e filtrar testes por tipo
- **Faker**: gerar dados dinâmicos em vez de valores fixos
- **Pydantic**: validar o schema completo da resposta JSON
- **Allure**: relatórios visuais com histórico de execuções
- **Autenticação**: testar APIs que exigem token ou API key
