# Uso

## Executando o dashboard

```bash
poetry run streamlit run src/f1/dashboard.py
```

A interface permite:

1. Selecionar o ano (dados historicos disponiveis a partir de 2023).
2. Selecionar o evento (Grande Premio) daquele ano.
3. Selecionar a sessao (treino, classificacao, corrida).
4. Ajustar o numero de pilotos exibidos no ranking (Top N).

A tabela resultante mostra a volta mais rapida de cada piloto na sessao
selecionada, ordenada da mais rapida para a mais lenta.

## Configuracao

Variaveis de ambiente (podem ser definidas em um arquivo `.env` local, nao
versionado):

| Variavel | Padrao | Descricao |
|---|---|---|
| `OPENF1_BASE_URL` | `https://api.openf1.org/v1` | URL base da API OpenF1 |
| `OPENF1_TIMEOUT_SECONDS` | `10` | Timeout das requisicoes HTTP |
| `OPENF1_MAX_RETRIES` | `3` | Numero de tentativas em caso de falha |
| `F1_LOG_LEVEL` | `INFO` | Nivel de log da aplicacao |
| `OPENF1_API_TOKEN` | (nenhum) | Token opcional para futuros endpoints de live timing |

Nenhuma credencial e necessaria para consumir os dados historicos da OpenF1.

## Rodando os testes

```bash
# Testes unitarios
poetry run pytest tests/unit/

# Com cobertura minima de 50%
poetry run pytest tests/unit/ --cov=src --cov-fail-under=50

# Testes de integracao (rede real)
poetry run pytest tests/integration/ -m integration
```
