CREATE TABLE IF NOT EXISTS clientes (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(120) NOT NULL
);

CREATE TABLE IF NOT EXISTS pecas (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(200) NOT NULL,
    codigo VARCHAR(100) NOT NULL UNIQUE,
    sku VARCHAR(100) NOT NULL UNIQUE,
    codigo_fabricante VARCHAR(100),
    descricao TEXT,
    categoria VARCHAR(120),
    fabricante VARCHAR(150),
    fornecedor VARCHAR(150),
    quantidade_estoque INTEGER NOT NULL DEFAULT 0 CHECK (quantidade_estoque >= 0),
    estoque_minimo INTEGER NOT NULL DEFAULT 0 CHECK (estoque_minimo >= 0),
    preco_custo NUMERIC(12, 2) NOT NULL DEFAULT 0,
    preco_venda NUMERIC(12, 2) NOT NULL DEFAULT 0,
    localizacao VARCHAR(120),
    status VARCHAR(20) NOT NULL DEFAULT 'ativo' CHECK (status IN ('ativo', 'inativo')),
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    ultima_atualizacao TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    deleted_at TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS movimentacoes_estoque (
    id SERIAL PRIMARY KEY,
    peca_id INTEGER NOT NULL REFERENCES pecas(id) ON DELETE RESTRICT,
    tipo VARCHAR(20) NOT NULL CHECK (tipo IN ('entrada', 'saida', 'ajuste')),
    quantidade_anterior INTEGER NOT NULL DEFAULT 0,
    quantidade_movimentada INTEGER NOT NULL,
    quantidade_final INTEGER NOT NULL,
    motivo VARCHAR(255),
    usuario_responsavel VARCHAR(150) NOT NULL DEFAULT 'sistema',
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_pecas_nome ON pecas (nome);
CREATE INDEX IF NOT EXISTS idx_pecas_codigo ON pecas (codigo);
CREATE INDEX IF NOT EXISTS idx_pecas_sku ON pecas (sku);
CREATE INDEX IF NOT EXISTS idx_pecas_fabricante ON pecas (fabricante);
CREATE INDEX IF NOT EXISTS idx_pecas_categoria ON pecas (categoria);
CREATE INDEX IF NOT EXISTS idx_pecas_status ON pecas (status);
CREATE INDEX IF NOT EXISTS idx_pecas_deleted_at ON pecas (deleted_at);
CREATE INDEX IF NOT EXISTS idx_movimentacoes_peca_id ON movimentacoes_estoque (peca_id);
CREATE INDEX IF NOT EXISTS idx_movimentacoes_created_at ON movimentacoes_estoque (created_at DESC);
