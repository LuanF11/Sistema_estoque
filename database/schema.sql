-- Tabela de Produtos
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL DEFAULT 0,
    valor_compra REAL NOT NULL,
    valor_venda REAL NOT NULL,
    data_validade DATE NULL,
    ativo INTEGER NOT NULL DEFAULT 1,
    estoque_minimo INTEGER NOT NULL DEFAULT 5,
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

-- INSERT INTO produtos (
--     nome,
--     quantidade,
--     valor_compra,
--     valor_venda,
--     data_validade,
--     ativo,
--     estoque_minimo,
--     data_cadastro
-- ) VALUES
-- -- 2024
-- ('Vaso Clássico Pequeno', 60, 8.00, 20.00, NULL, 1, 10, '2024-03-10 09:15:00'),
-- ('Substrato Universal 10kg', 30, 18.00, 35.00, '2025-12-01', 1, 8, '2024-06-22 14:40:00'),
-- ('Fertilizante Mineral 500ml', 12, 14.00, 30.00, '2025-10-15', 1, 5, '2024-09-05 11:10:00'),

-- -- 2025
-- ('Vaso Decorativo Luxo', 8, 50.00, 120.00, NULL, 1, 3, '2025-01-18 10:00:00'),
-- ('Adubo Orgânico Premium', 4, 22.00, 45.00, '2026-01-18', 1, 6, '2025-04-12 16:20:00'),
-- ('Ração Vegetal Especial', 2, 25.00, 48.00, '2025-12-28', 1, 5, '2025-07-30 13:50:00'),
-- ('Planta Bonsai Ficus', 6, 80.00, 160.00, NULL, 1, 2, '2025-10-08 09:30:00'),

-- -- 2026
-- ('Kit Jardinagem Avançado', 20, 35.00, 75.00, NULL, 1, 10, '2026-01-05 08:45:00'),
-- ('Fertilizante Líquido Ultra', 3, 28.00, 55.00, '2026-01-25', 1, 6, '2026-01-12 15:00:00'),
-- ('Substrato Premium 20kg', 1, 45.00, 90.00, '2026-01-22', 1, 5, '2026-01-14 17:10:00');


-- INSERT INTO produto_tag (produto_id, tag_id) VALUES
-- (12, 2),
-- (13, 8),
-- (14, 6),
-- (15, 7),
-- (16, 6),
-- (17, 5),
-- (18, 1),
-- (19, 8),
-- (20, 6),
-- (21, 8);


-- INSERT INTO movimentacoes (
--     produto_id,
--     tipo,
--     quantidade,
--     data_movimentacao,
--     observacao
-- ) VALUES
-- -- 2024
-- (12, 'ENTRADA', 60, '2024-03-10 09:20:00', 'Compra inicial'),
-- (13, 'ENTRADA', 30, '2024-06-22 15:00:00', 'Compra fornecedor'),
-- (14, 'ENTRADA', 12, '2024-09-05 11:30:00', 'Compra fornecedor'),

-- -- 2025
-- (15, 'ENTRADA', 8, '2025-01-18 10:15:00', 'Compra fornecedor'),
-- (16, 'ENTRADA', 10, '2025-04-12 16:30:00', 'Compra fornecedor'),
-- (17, 'ENTRADA', 6, '2025-07-30 14:00:00', 'Compra fornecedor'),
-- (18, 'ENTRADA', 6, '2025-10-08 10:00:00', 'Compra fornecedor'),

-- -- Vendas
-- (12, 'SAIDA', 20, '2024-05-15 16:40:00', 'Venda balcão'),
-- (13, 'SAIDA', 10, '2024-08-01 12:10:00', 'Venda balcão'),
-- (15, 'SAIDA', 5, '2025-02-10 14:00:00', 'Venda online'),
-- (16, 'SAIDA', 6, '2025-06-01 10:30:00', 'Venda balcão'),
-- (19, 'ENTRADA', 20, '2026-01-05 09:00:00', 'Compra fornecedor'),
-- (19, 'SAIDA', 5, '2026-01-10 11:45:00', 'Venda balcão'),
-- (20, 'ENTRADA', 10, '2026-01-12 15:10:00', 'Compra fornecedor'),
-- (21, 'ENTRADA', 5, '2026-01-14 17:20:00', 'Compra fornecedor'),
-- (20, 'SAIDA', 7, '2026-01-14 18:00:00', 'Venda urgente');


-- INSERT INTO tags (nome) VALUES
-- ('Plantas'),
-- ('Vasos'),
-- ('Suculentas'),
-- ('Carnívoras'),
-- ('Alimentos'),
-- ('Fertilizantes'),
-- ('Decoração'),
-- ('Jardinagem'),
-- ('Promoção');


-- INSERT INTO produtos (
--     nome,
--     quantidade,
--     valor_compra,
--     valor_venda,
--     data_validade,
--     ativo,
--     estoque_minimo
-- ) VALUES
-- -- 🟢 Sem validade
-- ('Vaso Cerâmica Grande', 40, 40.00, 80.00, NULL, 1, 10),
-- ('Vaso Plástico Simples', 3, 5.00, 15.00, NULL, 1, 10), -- ⚠️ estoque baixo
-- ('Planta Suculenta Mix', 8, 6.00, 18.00, NULL, 1, 10), -- ⚠️ estoque baixo

-- -- VENCIDOS
-- ('Fertilizante Orgânico 500ml', 4, 10.00, 22.00, '2025-12-10', 1, 5),
-- ('Ração Vegetal Básica', 2, 15.00, 30.00, '2025-11-20', 1, 5),

-- -- PERTO DE VENCER (≤ 7 dias)
-- ('Adubo Líquido Premium', 6, 18.00, 36.00, '2026-01-18', 1, 8),
-- ('Substrato Especial 3kg', 7, 12.00, 25.00, '2026-01-20', 1, 10),

-- -- VENCIDO + ESTOQUE BAIXO
-- ('Fertilizante Foliar', 1, 9.00, 20.00, '2025-12-01', 1, 5),

-- -- PERTO DE VENCER + ESTOQUE BAIXO
-- ('Ração Vegetal Premium', 3, 20.00, 38.00, '2026-01-19', 1, 5),

-- -- OK
-- ('Planta Carnívora Dionaea', 15, 18.00, 35.00, NULL, 1, 5),
-- ('Kit Jardinagem Básico', 25, 22.00, 50.00, NULL, 1, 10);


-- INSERT INTO produto_tag (produto_id, tag_id) VALUES
-- (1, 2), (1, 7),
-- (2, 2), (2, 9),
-- (3, 1), (3, 3),
-- (4, 6), (4, 8),
-- (5, 5),
-- (6, 6), (6, 9),
-- (7, 8),
-- (8, 6),
-- (9, 5), (9, 9),
-- (10, 1), (10, 4),
-- (11, 8);


-- INSERT INTO movimentacoes (
--     produto_id,
--     tipo,
--     quantidade,
--     observacao
-- ) VALUES
-- -- Entradas iniciais
-- (1, 'ENTRADA', 40, 'Compra fornecedor'),
-- (2, 'ENTRADA', 15, 'Compra fornecedor'),
-- (3, 'ENTRADA', 20, 'Compra fornecedor'),
-- (4, 'ENTRADA', 20, 'Lote antigo'),
-- (5, 'ENTRADA', 10, 'Lote antigo'),
-- (6, 'ENTRADA', 15, 'Compra recente'),
-- (7, 'ENTRADA', 15, 'Compra recente'),
-- (8, 'ENTRADA', 8, 'Compra antiga'),
-- (9, 'ENTRADA', 10, 'Compra recente'),
-- (10, 'ENTRADA', 20, 'Compra fornecedor'),
-- (11, 'ENTRADA', 25, 'Compra fornecedor'),

-- -- Saídas (vendas)
-- (2, 'SAIDA', 12, 'Vendas balcão'),
-- (3, 'SAIDA', 12, 'Promoção'),
-- (4, 'SAIDA', 16, 'Vendas antigas'),
-- (5, 'SAIDA', 8, 'Vendas antigas'),
-- (6, 'SAIDA', 9, 'Venda rápida'),
-- (7, 'SAIDA', 8, 'Venda rápida'),
-- (8, 'SAIDA', 7, 'Vendas antigas'),
-- (9, 'SAIDA', 7, 'Promoção'),
-- (10, 'SAIDA', 5, 'Venda online');

