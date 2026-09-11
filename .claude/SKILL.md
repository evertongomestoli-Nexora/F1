# SKILL.md — Padrão Técnico para Projetos Python de Engenharia de Dados

Este documento define regras e boas práticas obrigatórias para criação, manutenção e evolução de
projetos Python no time de Engenharia de Dados. Desenvolvedores e agentes de IA devem seguir
estas diretrizes de forma consistente.

## 1. Gerenciamento do Projeto

- Utilizar **Poetry** para gerenciamento do projeto Python.
- Utilizar **Poetry** para gerenciamento de dependências.
- **Nunca** utilizar `pip` para instalar ou gerenciar dependências do projeto.
- Todas as dependências devem ser declaradas e controladas pelo Poetry através do `pyproject.toml`.
- Alterações de dependências devem sempre passar por `poetry add`, `poetry remove` ou edição
  explícita do `pyproject.toml` seguida de `poetry lock`.

## 2. Pyenv

- Utilizar **pyenv** para gerenciamento da versão local do Python.
- A versão do Python utilizada pelo projeto deve ser definida explicitamente (arquivo
  `.python-version` e/ou `python = ">=X.Y"` no `pyproject.toml`).
- O projeto deve possuir configuração que permita reproduzir a mesma versão do Python em
  diferentes ambientes.
- Antes de executar comandos relacionados ao projeto, verificar se a versão correta do Python
  está sendo utilizada (`pyenv version`, `python --version`).

## 3. Estrutura do Projeto

- Utilizar uma estrutura organizada e modular.
- Utilizar a estrutura `src/` para o código-fonte do projeto.
- Separar adequadamente código-fonte, testes, documentação e configurações:

```
projeto/
├── src/
│   └── <pacote>/
│       ├── domain/
│       ├── ingestion/
│       ├── processing/
│       └── utils/
├── tests/
│   ├── unit/
│   └── integration/
├── docs/
├── pyproject.toml
├── .python-version
└── SKILL.md
```

- Evitar arquivos excessivamente grandes e responsabilidades misturadas.
- Seguir princípios de código limpo, baixo acoplamento e alta coesão (ex.: separar camadas de
  domínio, ingestão/processamento e apresentação, com dependência sempre apontando para o
  domínio).

## 4. Lint e Formatação

- Utilizar **Ruff** para linting e formatação do código Python.
- O Ruff deve ser utilizado para verificar erros, padrões de código e organização dos imports.
- O código deve ser formatado (`ruff format`) antes de ser considerado pronto.
- Não ignorar erros do Ruff (`# noqa`, exclusões em `pyproject.toml`) sem uma justificativa
  técnica explícita documentada em comentário ou commit.

## 5. Testes

- Utilizar **pytest** para testes automatizados.
- Criar testes unitários para o código do projeto.
- A cobertura mínima obrigatória deve ser de **50%** do código localizado em `src/`.
- Os testes devem ser executados automaticamente sempre que possível (CI, pre-commit, hooks).
- Código novo ou alterado deve possuir testes adequados.
- Não reduzir deliberadamente a cobertura existente para fazer o pipeline passar.
- Testes que dependem de serviços externos (ex.: APIs ao vivo) devem ser isolados com marcadores
  (ex.: `@pytest.mark.integration`) e não devem rodar no pipeline padrão de testes unitários.

## 6. Documentação

- Utilizar **MkDocs** para criação e manutenção da documentação do projeto.
- A documentação deve permanecer versionada junto ao código (diretório `docs/`).
- Documentar instalação, configuração, utilização, arquitetura e principais componentes do
  projeto.
- Funções, classes e módulos relevantes devem possuir docstrings/documentação adequada.

## 7. Boas Práticas

- Utilizar type hints sempre que aplicável.
- Seguir PEP 8 e boas práticas modernas de Python.
- Utilizar nomes claros e descritivos para variáveis, funções, classes e módulos.
- Evitar código duplicado.
- Evitar complexidade desnecessária.
- Separar configuração de lógica de negócio (ex.: módulo `config.py` dedicado).
- Implementar tratamento adequado de erros e exceções.
- Utilizar logging quando necessário, evitando `print` em código de produção.
- **Nunca** armazenar senhas, tokens ou chaves de API diretamente no código — utilizar variáveis
  de ambiente ou gerenciadores de segredo.

## 8. Comportamento do Agente de IA

Antes de modificar qualquer projeto, o agente deve:

- Inspecionar a estrutura existente.
- Verificar o `pyproject.toml`.
- Verificar a versão do Python configurada pelo pyenv.
- Verificar as dependências existentes.
- Verificar as configurações do Ruff.
- Verificar a estrutura e cobertura dos testes.
- Verificar a documentação existente.

O agente deve preservar os padrões já existentes no projeto e evitar alterações desnecessárias.

O agente **nunca** deve:

- Utilizar `pip` quando o projeto utiliza Poetry.
- Alterar a versão do Python sem justificativa.
- Adicionar dependências sem necessidade.
- Ignorar testes ou erros de lint apenas para concluir uma tarefa.
- Remover testes existentes sem justificativa.
- Colocar credenciais ou segredos no código.

## 9. Validação Final

Antes de considerar qualquer alteração concluída, executar, quando aplicável:

```bash
# Validação do projeto com Poetry
poetry check

# Verificação da versão do Python
pyenv version
python --version

# Lint
poetry run ruff check .

# Formatação
poetry run ruff format --check .

# Testes
poetry run pytest tests/unit/

# Cobertura mínima de 50%
poetry run pytest tests/unit/ --cov=src --cov-fail-under=50

# Documentação MkDocs
poetry run mkdocs build
```

## 10. Checklist de Conformidade

- [ ] Poetry está sendo utilizado para gerenciamento do projeto.
- [ ] Nenhuma dependência foi instalada utilizando pip.
- [ ] A versão do Python está definida e controlada pelo pyenv.
- [ ] O projeto utiliza estrutura `src/`.
- [ ] Ruff está configurado e executando corretamente.
- [ ] O código está formatado.
- [ ] Pytest está configurado.
- [ ] A cobertura de testes é de pelo menos 50% do código em `src/`.
- [ ] MkDocs está configurado.
- [ ] A documentação está atualizada.
- [ ] Não existem secrets no código.
- [ ] O projeto possui estrutura modular.
- [ ] As alterações foram validadas antes da conclusão.
