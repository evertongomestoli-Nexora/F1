# Plano: Criação do Projeto F1 (Dashboard OpenF1)

## Contexto

O repositório hoje tem apenas o scaffolding mínimo (`pyproject.toml`, `.python-version`,
`src/f1/__init__.py`, `tests/__init__.py`, `SKILL.md`, `doc_api.md`). O `CLAUDE.md` já descreve a
arquitetura-alvo (camadas domain/ingestion/processing/utils + dashboard Streamlit), mas nenhum
desses módulos existe ainda. O objetivo deste plano é construir o projeto do zero seguindo:

- **[SKILL.md](SKILL.md)** — padrão técnico obrigatório (Poetry, pyenv, `src/`, Ruff, pytest ≥50%
  cobertura, MkDocs, boas práticas, sem secrets no código).
- **[doc_api.md](doc_api.md)** — contrato da OpenF1 API que a camada de ingestão deve consumir
  (`/meetings`, `/sessions`, `/laps`, `/drivers`, sem autenticação para dados históricos, filtros
  via query params, `latest` para sessão/evento mais recente).
- **CLAUDE.md** (já existente no repo) — arquitetura em camadas (domain ← ingestion/processing ←
  UI) e comandos de projeto já definidos (poetry install, pytest, ruff, streamlit run
  `src/f1/dashboard.py`, mkdocs).

Resultado esperado: um dashboard Streamlit funcional que exibe voltas mais rápidas por
piloto/sessão de F1, com arquitetura limpa, testada e documentada, pronto para evoluir.

## Abordagem

Construir de baixo para cima: domínio → ingestão → processamento → composição (dashboard) → testes
→ documentação, validando a cada camada.

### 1. Dependências (Poetry)

Adicionar ao `pyproject.toml` via `poetry add`:
- Runtime: `pydantic` (>=2), `httpx` (cliente HTTP), `streamlit` (`<2.0.0` conforme CLAUDE.md),
  `pandas` (<3), `python-dotenv` (config via env vars).
- Dev (`poetry add --group dev`): `pytest`, `pytest-cov`, `ruff`, `mkdocs`, `mkdocs-material`,
  `pre-commit`, `taskipy` (para `poetry run task docs`).

Configurar `[tool.ruff]`, `[tool.pytest.ini_options]` (markers `integration`), `[tool.coverage]`
(`fail_under = 50`, `source = ["src"]`) e `[tool.taskipy.tasks]` (`docs`, `docs-build`) no
`pyproject.toml`.

### 2. Camada `domain/` (sem dependências externas)

- `src/f1/domain/models.py` — modelos Pydantic v2: `Meeting`, `Session`, `Lap`, `Driver`,
  `FastestLapEntry`, mapeando os campos relevantes dos endpoints `/meetings`, `/sessions`,
  `/laps`, `/drivers` descritos em [doc_api.md](doc_api.md).
- `src/f1/domain/repositories.py` — ABCs: `MeetingRepository`, `SessionRepository`,
  `LapRepository`, `DriverRepository`, cada uma com métodos de busca (ex.:
  `list_by_year`, `list_by_session_key`).
- `src/f1/domain/services.py` — `F1DashboardService`, recebendo os 4 repositórios abstratos via
  injeção de dependência, orquestrando busca + chamadas às funções puras de `processing/`.

### 3. Camada `ingestion/` (adapters OpenF1)

- `src/f1/ingestion/http_client.py` — `HttpClient` fino sobre `httpx`, com retry/backoff (ex.:
  `tenacity` ou implementação manual simples) e helper para montar query params (incluindo
  suporte a operadores `>`, `>=`, `<`, `<=` e `latest`, conforme doc_api.md).
- `src/f1/ingestion/openf1_client.py` — implementações concretas das ABCs de `domain/repositories`
  chamando `https://api.openf1.org/v1/{meetings,sessions,laps,drivers}`; cada item que falhar na
  validação Pydantic é logado e descartado (não aborta a página inteira), conforme decisão de
  design do CLAUDE.md.

### 4. Camada `processing/` (funções puras, sem I/O)

- `src/f1/processing/lap_processor.py` — `filter_valid_laps`, `build_driver_index`,
  `compute_top_n_laps`. Zero efeitos colaterais para permitir testes unitários sem mocks.

### 5. Config e Logging (`utils/`)

- `src/f1/utils/config.py` — loader de configuração via env vars (`.env` + `python-dotenv`),
  ex.: `OPENF1_BASE_URL`, timeouts, nível de log. Nenhum segredo hardcoded (a API pública não
  exige chave, mas o padrão deve suportar `OPENF1_API_TOKEN` opcional para live timing futuro).
- `src/f1/utils/logger.py` — `get_logger(name)` factory usando `logging` padrão.

### 6. Composição (`dashboard.py`)

- `src/f1/dashboard.py` — composition root Streamlit: instancia `HttpClient`, os 4 repositórios
  concretos, `F1DashboardService`, e monta a UI (seleção de ano/evento/sessão, tabela de voltas
  mais rápidas). Usa `@st.cache_resource` para os repositórios/serviço e `@st.cache_data` para os
  resultados de busca, sem lógica de negócio no arquivo.

### 7. Testes

- `tests/unit/test_lap_processor.py` — cobre as funções puras de `processing/` (sem mocks).
- `tests/unit/test_services.py` — testa `F1DashboardService` com repositórios fake/mock (dublês
  simples implementando as ABCs, não `unittest.mock` genérico, para manter testes legíveis).
- `tests/unit/test_domain_models.py` — validação dos modelos Pydantic com payloads de exemplo
  baseados nos endpoints do doc_api.md.
- `tests/integration/test_openf1_client.py`, marcado `@pytest.mark.integration`, batendo na API
  real (`/meetings?year=2023`, etc.), excluído do `pytest tests/unit/`.
- Rodar `poetry run pytest tests/unit/ --cov=src --cov-fail-under=50` e garantir ≥50% de
  cobertura em `src/`.

### 8. Documentação (MkDocs)

- `mkdocs.yml` na raiz + `docs/index.md`, `docs/instalacao.md`, `docs/arquitetura.md`,
  `docs/uso.md` cobrindo instalação (Poetry/pyenv), configuração, uso do dashboard e a arquitetura
  em camadas (referenciando o diagrama já existente no CLAUDE.md).
- Adicionar tarefas `docs` / `docs-build` via taskipy, conforme comando já citado no CLAUDE.md
  (`poetry run task docs`).

### 9. Qualidade e hooks

- `.pre-commit-config.yaml` com hooks: `ruff` (lint + format), `trailing-whitespace`,
  `check-yaml`, `check-toml` — igual ao já descrito no CLAUDE.md.
- Garantir `README.md` permaneça ASCII-only (checar antes de editar).

## Ordem de execução sugerida

1. Configurar dependências e seções de ferramentas no `pyproject.toml`.
2. Implementar `domain/` (models → repositories → services).
3. Implementar `processing/lap_processor.py` + testes unitários (validação rápida, sem I/O).
4. Implementar `ingestion/` (http_client → openf1_client).
5. Implementar `utils/` (config, logger).
6. Implementar `dashboard.py` (composition root).
7. Escrever testes unitários restantes + teste de integração marcado.
8. Configurar MkDocs e escrever documentação.
9. Configurar `.pre-commit-config.yaml`.
10. Rodar validação final completa (seção 9 do SKILL.md).

## Verificação

```bash
poetry install --with dev
pyenv version                     # deve reportar 3.12.10
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest tests/unit/ --cov=src --cov-fail-under=50
poetry run pytest tests/integration/ -m integration   # opcional, requer rede
poetry run task docs-build
poetry run streamlit run src/f1/dashboard.py           # validação manual da UI
```

Confirmar ao final o checklist de conformidade do [SKILL.md](SKILL.md) (item 10).
