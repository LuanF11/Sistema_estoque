-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    valor_comprado REAL NOT NULL,
    valor_venda REAL NOT NULL,
    data_validade DATE NULL,
    ativo INTEGER NOT NULL DEFAULT 1,
    data_cadastro DATETIME DEFAULT CURRENT_TIMESTAMP

);

-- Tabela de Tags
CREATE TABLE IF NOT EXISTS tags(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL UNIQUE

);

--Tabela de relacionamento entre Produtos e Tags (N:N)
CREATE TABLE IF NOT EXISTS produto_tag(
    produto_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    PRIMARY KEY (produto_id, tag_id),
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Tabela de Movimentações de Estoque
CREATE TABLE IF NOT EXISTS movimentacoes(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    produto_id INTEGER NOT NULL,
    tipo TEXT NOT NULL CHECK(tipo IN ('ENTRADA', 'SAIDA')),
    quantidade INTEGER NOT NULL,
    data_movimentacao DATETIME DEFAULT CURRENT_TIMESTAMP,
    observacao TEXT,
    FOREIGN KEY (produto_id) REFERENCES produtos(id) ON DELETE CASCADE

);
