# Instalacao

## Pre-requisitos

- [pyenv](https://github.com/pyenv-win/pyenv-win) com Python 3.12 instalado
  (versao fixada em `.python-version`).
- [Poetry](https://python-poetry.org/) para gerenciamento de dependencias.

## Passos

1. Confirme a versao do Python:

   ```bash
   pyenv version
   python --version
   ```

2. Instale as dependencias do projeto (runtime + dev):

   ```bash
   poetry install --with dev
   ```

3. (Opcional) Configure variaveis de ambiente criando um arquivo `.env` na
   raiz do projeto (veja as chaves em [Uso](uso.md#configuracao)).

4. Ative os hooks de pre-commit:

   ```bash
   poetry run pre-commit install
   ```

## Verificacao

```bash
poetry run ruff check .
poetry run ruff format --check .
poetry run pytest tests/unit/ --cov=src --cov-fail-under=50
```
