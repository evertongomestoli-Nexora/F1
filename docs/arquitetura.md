# Arquitetura

O projeto segue uma arquitetura em camadas (clean/layered), com a regra de
dependencia sempre apontando para o dominio:

```
UI (dashboard.py) -> Domain <- Ingestion / Processing
```

```
src/f1/
|-- dashboard.py          # Streamlit composition root - monta as dependencias, sem logica de negocio
|-- domain/                # Camada central, sem dependencias externas
|   |-- models.py          # Modelos Pydantic v2: Meeting, Session, Lap, Driver, FastestLapEntry
|   |-- repositories.py    # ABCs (interfaces) para acesso a dados
|   `-- services.py        # F1DashboardService - orquestra repositorios e processamento
|-- ingestion/              # Adapters da OpenF1 API implementando as ABCs de dominio
|   |-- http_client.py     # HttpClient com retry/backoff
|   `-- openf1_client.py   # Implementacoes concretas dos repositorios (Meeting, Session, Lap, Driver)
|-- processing/             # Funcoes puras, sem I/O
|   `-- lap_processor.py   # filter_valid_laps, build_driver_index, compute_top_n_laps
`-- utils/
    |-- config.py           # Loader de configuracao via variaveis de ambiente
    `-- logger.py           # Factory get_logger
```

## Decisoes de design

- `F1DashboardService` depende apenas dos repositorios abstratos, permitindo
  trocar implementacoes livremente (por exemplo, em testes, com fakes).
- `lap_processor.py` nao possui efeitos colaterais; todos os testes unitarios
  dessa camada nao exigem mocks.
- Os repositorios em `openf1_client.py` descartam (com log) itens que falham
  na validacao Pydantic, em vez de abortar a busca inteira por causa de um
  unico item invalido.
- `dashboard.py` usa `@st.cache_resource` para os repositorios/servico e
  `@st.cache_data` para os resultados de busca, evitando re-fetch a cada
  re-render do Streamlit.
