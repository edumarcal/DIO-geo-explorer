# DIO-geo-explorer

Geo Explorer é um projeto de estudo e portfólio que ajuda a pessoa usuária a explorar trilhas de aprendizagem, receber desafios de código e gerar um certificado fictício ao concluir uma rota de estudo.

## Objetivo

O projeto simula um ambiente de aprendizagem com três principais fluxos:

- Trilha: apresenta um plano de estudos por tecnologia.
- Desafio: gera um exercício prático com base na tecnologia e no nível informado.
- Certificado: cria um certificado fictício de conclusão.

## Estrutura do projeto

```text
geo_explorer/
├── __init__.py
├── cli.py
├── data/
│   └── trilhas.json
├── data_loader.py
├── mcp_server.py
└── services.py
main.py
tests/
└── test_geo_explorer.py
README.md
pyproject.toml
```

## Como executar

### Opção 1: via Python diretamente

```bash
python main.py listar
python main.py trilha --tecnologia python
python main.py desafio --tecnologia python --nivel intermediario
python main.py certificado --nome "Maria Silva" --tecnologia python --trilha "Python para Iniciantes"
```

### Opção 2: via módulo

```bash
python -m geo_explorer.cli listar
python -m geo_explorer.cli trilha --tecnologia python
python -m geo_explorer.cli desafio --tecnologia javascript --nivel iniciante
python -m geo_explorer.cli certificado --nome "Maria Silva" --tecnologia javascript --trilha "JavaScript moderno"
```

### Opção 3: interface web local

```bash
python app.py
```

Acesse em `http://127.0.0.1:8000` para visualizar a interface com trilha, desafio e certificado em uma página simples.

### Opção 4: instalar como comando

```bash
pip install -e .
geo-explorer listar
geo-explorer trilha --tecnologia python
```

## Como usar os comandos

### listar

Exibe todas as tecnologias disponíveis no banco fictício do projeto.

### trilha

Recebe uma tecnologia e mostra:

- nome da trilha;
- descrição;
- duração;
- nível;
- módulos;
- objetivos.

### desafio

Recebe uma tecnologia e um nível e gera:

- título do desafio;
- descrição;
- requisitos;
- dica de desenvolvimento.

### certificado

Recebe o nome da pessoa, a tecnologia e o nome da trilha e gera um certificado fictício com código e assinatura.

## Servidor MCP

O projeto também inclui um servidor MCP em stdio, que expõe as ferramentas do Geo Explorer para clientes compatíveis com MCP.

Para iniciar o servidor manualmente:

```bash
python -m geo_explorer.mcp_server
```

A configuração pronta para VS Code está em `.vscode/mcp.json`.

## Como executar os testes

```bash
python -m pytest -q
```

## Melhorias extras implementadas

- base de trilhas fictícias em arquivo JSON;
- estrutura organizada em módulos e serviços;
- testes automatizados para validar as funções e a CLI;
- servidor MCP leve em modo STDIO para expor as ferramentas;
- documentação para execução de exemplos reais.

## O que aprendi

Durante a implementação do projeto, foi possível praticar:

- organização de projetos em Python;
- criação de dados fictícios e carregamento em arquivos JSON;
- desenvolvimento de CLI com subcomandos;
- geração de relatórios e certificados;
- validação com testes automatizados;
- integração com um modelo simples de servidor MCP.

## Observação

Este projeto foi criado como exemplo de portfólio, com dados fictícios e foco em aprendizado prático.
