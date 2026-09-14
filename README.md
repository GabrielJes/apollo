# Apollo

Estrutura MVC simples para cadastro e consulta de jogadores.

## Estrutura

```text
app/
├── controllers/       # Coordena as regras do fluxo
├── models/            # Entidades do dominio
├── repositories/      # Persistencia dos dados
└── views/             # Frontend React
tests/                 # Testes automatizados
```

O frontend React fica em `app/views/frontend`. O build e feito automaticamente
na etapa Node do `Dockerfile` e servido pelo Flask na mesma origem da API.

## Executar

```bash
python3 -m unittest discover -s tests -v
```

O backend e executado pelo `web.py`. Os jogadores sao persistidos no PostgreSQL.

## Executar com Docker

```bash
docker-compose up --build
docker-compose up --build --scale app=2
```

O Nginx fica disponivel em `http://localhost` e encaminha as requisicoes para o
servico `app`. O Postgres usa o volume `postgres_data` e fica acessivel apenas
pela rede interna do Compose.
