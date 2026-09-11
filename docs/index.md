# F1 Dashboard

Dashboard Streamlit que exibe as voltas mais rapidas por piloto/sessao de
Formula 1, consumindo a [OpenF1 API](https://openf1.org).

O projeto segue uma arquitetura em camadas limpa:

```
UI (dashboard.py) -> Domain <- Ingestion / Processing
```

## Features

- **Dashboard interativo** construido com Streamlit para explorar voltas mais rapidas por piloto e sessao.
- **Integracao com a OpenF1 API** atraves de repositorios de ingestao com retry/backoff.
- **Arquitetura em camadas** (UI -> Domain <- Ingestion/Processing), com o dominio isolado de dependencias externas.
- **Processamento puro e sem efeitos colaterais** para filtragem e ranking de voltas, o que facilita testes.
- **Tolerancia a falhas parciais**: itens invalidos retornados pela API sao logados e ignorados sem interromper o carregamento.
- **Cache de dados e recursos** via `@st.cache_resource` / `@st.cache_data` para evitar novas chamadas a API em cada re-renderizacao.
- **Suite de testes** unitarios e de integracao, com cobertura minima garantida em CI.

## Quick Start

Instale as dependencias do projeto (incluindo as de desenvolvimento):

```bash
poetry install --with dev
```

Execute o dashboard:

```bash
poetry run streamlit run src/f1/dashboard.py
```

## Available Tasks

Comandos disponiveis via `poetry run task <nome>` (definidos em `pyproject.toml`):

| Tarefa | Comando | Descricao |
| --- | --- | --- |
| `test` | `poetry run task test` | Executa os testes unitarios com cobertura minima de 50%. |
| `test-all` | `poetry run task test-all` | Executa os testes unitarios e de integracao com cobertura minima de 50%. |
| `lint` | `poetry run task lint` | Verifica o codigo com o ruff sem aplicar correcoes. |
| `lint-fix` | `poetry run task lint-fix` | Verifica o codigo com o ruff e corrige automaticamente o que for possivel. |
| `format` | `poetry run task format` | Formata o codigo com o ruff format. |
| `docs` | `poetry run task docs` | Serve a documentacao localmente com o mkdocs. |
| `docs-build` | `poetry run task docs-build` | Gera a build estatica da documentacao com o mkdocs. |

Consulte:

- [Instalacao](instalacao.md) para configurar o ambiente.
- [Arquitetura](arquitetura.md) para entender as camadas do projeto.
- [Uso](uso.md) para aprender a usar o dashboard.
