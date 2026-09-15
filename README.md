# Apollo

Aplicacao web para gestao de clientes e estoque de pecas de uma oficina mecanica.

## Estrutura do projeto

```text
app/
├── controllers/       # Regras de fluxo e validacao
├── models/            # Entidades do dominio
├── repositories/      # Persistencia no banco de dados
├── views/             # Frontend React
│   └── frontend/
│       ├── src/
│       ├── package.json
│       └── vite.config.js
├── __init__.py
├── ...
database/
├── init.sql           # Schema inicial do banco
nginx/
├── nginx.conf
requirements.txt
web.py                 # Aplicacao Flask
Dockerfile
docker-compose.yml
tests/
└── test_cliente_controller.py
```

O frontend React fica em `app/views/frontend`. O build e feito automaticamente na etapa Node do `Dockerfile` e servido pelo Flask na mesma origem da API.

## Executar

```bash
python3 -m unittest discover -s tests -v
```

O backend e executado pelo `web.py`.

## Executar com Docker

```bash
sudo docker-compose up --build
sudo docker-compose up --build --scale app=2
```

O Nginx fica disponivel em `http://localhost` e encaminha as requisicoes para o servico `app`. O Postgres usa o volume `postgres_data` e fica acessivel apenas pela rede interna do Compose.

## Banco de dados

O banco utilizado e PostgreSQL. O schema principal e carregado por `database/init.sql` e inclui as seguintes tabelas.

### 1. clientes

Tabela para cadastro de clientes da oficina.

Campos principais:
- `id` - identificador unico
- `nome` - nome do cliente

Relacionamento:
- Nao possui relacionamentos diretos com as outras tabelas neste momento.

### 2. pecas

Tabela principal para o controle de estoque de pecas.

Campos principais:
- `id` - identificador unico
- `nome` - nome da peca
- `codigo` - codigo unico da peca
- `sku` - identificador unico do fornecedor/produto
- `codigo_fabricante` - codigo do fabricante
- `descricao` - descricao detalhada
- `categoria` - categoria da peca
- `fabricante` - fabricante da peca
- `fornecedor` - fornecedor da peca
- `quantidade_estoque` - quantidade atual em estoque
- `estoque_minimo` - estoque minimo recomendado
- `preco_custo` - preco de custo
- `preco_venda` - preco de venda
- `localizacao` - setor/localizacao no estoque
- `status` - status da peca (`ativo` ou `inativo`)
- `created_at` - data de criacao
- `ultima_atualizacao` - ultima data de alteracao
- `deleted_at` - marca logica de exclusao

Relacionamentos:
- `pecas` e referenciada por `movimentacoes_estoque` via `peca_id`.
- Possui indice para busca por nome, codigo, SKU, fabricante, categoria e status.

### 3. movimentacoes_estoque

Tabela de auditoria das movimentacoes de estoque.

Campos principais:
- `id` - identificador unico
- `peca_id` - referencia a peca movimentada
- `tipo` - tipo da movimentacao (`entrada`, `saida`, `ajuste`)
- `quantidade_anterior` - quantidade antes da movimentacao
- `quantidade_movimentada` - quantidade movimentada
- `quantidade_final` - quantidade final apos a movimentacao
- `motivo` - motivo da movimentacao
- `usuario_responsavel` - usuario responsavel pela operacao
- `created_at` - data da movimentacao

Relacionamentos:
- `movimentacoes_estoque.peca_id` -> `pecas.id`
- Cada alteracao de estoque gera um registro nesta tabela para rastreabilidade.

## Relacao entre tabelas

```text
clientes
  └── (sem relacionamento direto no schema atual)

pecas
  └── 1:N ──> movimentacoes_estoque
```

Em resumo:
- `clientes` armazena clientes da oficina.
- `pecas` guarda os itens de estoque.
- `movimentacoes_estoque` registra todas as entradas, saidas e ajustes de cada peca.

## Observacoes

- A tabela `pecas` usa `deleted_at` para exclusao logica, mantendo o registro historico.
- A tabela `movimentacoes_estoque` e usada para auditoria e acompanhamento do fluxo de estoque.
- O schema e criado automaticamente pela inicializacao do banco em `docker-compose.yml`.
