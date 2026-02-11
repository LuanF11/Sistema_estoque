from repositories.base_repository import BaseRepository


class AnalyticsRepository(BaseRepository):
    """Repositório para consultas analíticas avançadas"""

    def get_sales_by_period(self, start_date, end_date):
        """Vendas por dia no período"""
        query = """
        SELECT 
            DATE(m.data_movimentacao) as data,
            SUM(m.quantidade * p.valor_venda) as faturamento,
            SUM(m.quantidade * (p.valor_venda - p.valor_compra)) as lucro
        FROM movimentacoes m
        JOIN produtos p ON p.id = m.produto_id
        WHERE m.tipo = 'SAIDA' 
          AND DATE(m.data_movimentacao) BETWEEN DATE(?) AND DATE(?)
        GROUP BY DATE(m.data_movimentacao)
        ORDER BY data
        """
        return self.fetchall(query, (start_date, end_date))

    def get_top_products(self, limit=10):
        """Produtos mais vendidos"""
        query = """
        SELECT 
            p.id,
            p.nome,
            SUM(m.quantidade) as total_vendido,
            SUM(m.quantidade * p.valor_venda) as faturamento,
            SUM(m.quantidade * (p.valor_venda - p.valor_compra)) as lucro
        FROM movimentacoes m
        JOIN produtos p ON p.id = m.produto_id
        WHERE m.tipo = 'SAIDA'
        GROUP BY p.id, p.nome
        ORDER BY total_vendido DESC
        LIMIT ?
        """
        return self.fetchall(query, (limit,))

    def get_products_by_category(self):
        """Vendas por categoria (tag)"""
        query = """
        SELECT 
            t.nome as categoria,
            COUNT(DISTINCT p.id) as total_produtos,
            SUM(m.quantidade) as total_vendido,
            SUM(m.quantidade * p.valor_venda) as faturamento,
            SUM(m.quantidade * (p.valor_venda - p.valor_compra)) as lucro
        FROM produto_tag pt
        JOIN tags t ON t.id = pt.tag_id
        JOIN produtos p ON p.id = pt.produto_id
        LEFT JOIN movimentacoes m ON m.produto_id = p.id AND m.tipo = 'SAIDA'
        GROUP BY t.id, t.nome
        ORDER BY faturamento DESC
        """
        return self.fetchall(query)

    def get_stock_value(self):
        """Valor total do estoque"""
        query = """
        SELECT 
            SUM(quantidade * valor_compra) as valor_total_custo,
            SUM(quantidade * valor_venda) as valor_total_venda,
            COUNT(DISTINCT id) as total_produtos,
            SUM(quantidade) as total_itens
        FROM produtos
        WHERE ativo = 1
        """
        return self.fetchone(query)

    def get_low_stock_products(self):
        """Produtos com estoque baixo"""
        query = """
        SELECT 
            id,
            nome,
            quantidade,
            estoque_minimo,
            valor_venda
        FROM produtos
        WHERE ativo = 1 
          AND quantidade <= estoque_minimo
        ORDER BY quantidade ASC
        """
        return self.fetchall(query)

    def get_product_turnover(self, days=30):
        """Rotatividade de produtos (últimos N dias)"""
        query = """
        SELECT 
            p.id,
            p.nome,
            COUNT(m.id) as num_movimentacoes,
            SUM(CASE WHEN m.tipo = 'SAIDA' THEN m.quantidade ELSE 0 END) as total_saidas,
            SUM(CASE WHEN m.tipo = 'ENTRADA' THEN m.quantidade ELSE 0 END) as total_entradas
        FROM movimentacoes m
        JOIN produtos p ON p.id = m.produto_id
        WHERE DATE(m.data_movimentacao) >= DATE('now', '-' || ? || ' days')
        GROUP BY p.id, p.nome
        HAVING num_movimentacoes > 0
        ORDER BY total_saidas DESC
        """
        return self.fetchall(query, (days,))

    def get_profit_margin_by_product(self):
        """Margem de lucro por produto"""
        query = """
        SELECT 
            p.id,
            p.nome,
            p.valor_compra,
            p.valor_venda,
            ROUND(((p.valor_venda - p.valor_compra) / p.valor_venda * 100), 2) as margem_percentual,
            SUM(m.quantidade) as total_vendido,
            SUM(m.quantidade * (p.valor_venda - p.valor_compra)) as lucro_total
        FROM produtos p
        LEFT JOIN movimentacoes m ON m.produto_id = p.id AND m.tipo = 'SAIDA'
        WHERE p.ativo = 1
        GROUP BY p.id, p.nome
        ORDER BY margem_percentual DESC
        """
        return self.fetchall(query)

    def get_expiring_products(self, days=30):
        """Produtos próximos do vencimento"""
        query = """
        SELECT 
            id,
            nome,
            data_validade,
            quantidade,
            valor_venda,
            CAST((julianday(data_validade) - julianday('now')) AS INTEGER) as dias_para_vencer
        FROM produtos
        WHERE data_validade IS NOT NULL
          AND ativo = 1
          AND data_validade <= DATE('now', '+' || ? || ' days')
        ORDER BY data_validade ASC
        """
        return self.fetchall(query, (days,))

    def get_inactive_products(self, days=60):
        """Produtos sem movimentação (encalhados)"""
        query = """
        SELECT 
            p.id,
            p.nome,
            p.quantidade,
            p.data_cadastro,
            p.valor_venda,
            CASE 
                WHEN MAX(m.id) IS NOT NULL THEN
                    CAST((julianday(DATE('now')) - julianday(DATE(MAX(m.data_movimentacao)))) AS INTEGER)
                ELSE
                    CAST((julianday(DATE('now')) - julianday(DATE(p.data_cadastro))) AS INTEGER)
            END as dias_sem_movimento
        FROM produtos p
        LEFT JOIN movimentacoes m ON p.id = m.produto_id
        WHERE p.ativo = 1
        GROUP BY p.id, p.nome, p.data_cadastro
        HAVING dias_sem_movimento > ?
        ORDER BY dias_sem_movimento DESC
        """
        return self.fetchall(query, (days,))

    def get_monthly_summary(self, months=12):
        """Resumo mensal de vendas e lucro"""
        query = """
        SELECT 
            strftime('%Y-%m', m.data_movimentacao) as mes,
            SUM(CASE WHEN m.tipo = 'SAIDA' THEN m.quantidade ELSE 0 END) as qtd_vendida,
            SUM(CASE WHEN m.tipo = 'SAIDA' THEN m.quantidade * p.valor_venda ELSE 0 END) as faturamento,
            SUM(CASE WHEN m.tipo = 'SAIDA' THEN m.quantidade * (p.valor_venda - p.valor_compra) ELSE 0 END) as lucro
        FROM movimentacoes m
        JOIN produtos p ON p.id = m.produto_id
        WHERE m.data_movimentacao >= DATE('now', '-' || ? || ' months')
        GROUP BY strftime('%Y-%m', m.data_movimentacao)
        ORDER BY mes DESC
        """
        return self.fetchall(query, (months,))

    def get_cash_flow_summary(self, start_date, end_date):
        """Resumo de fluxo de caixa"""
        query = """
        SELECT 
            DATE(c.data) as data,
            c.valor_abertura,
            c.valor_fechamento,
            COALESCE(SUM(m.quantidade * p.valor_venda), 0) as vendas_total
        FROM caixa c
        LEFT JOIN movimentacoes m ON DATE(m.data_movimentacao) = c.data AND m.tipo = 'SAIDA'
        LEFT JOIN produtos p ON p.id = m.produto_id
        WHERE DATE(c.data) BETWEEN DATE(?) AND DATE(?)
        GROUP BY DATE(c.data)
        ORDER BY data DESC
        """
        return self.fetchall(query, (start_date, end_date))

    def get_total_statistics(self):
        """Estatísticas gerais do sistema"""
        query = """
        SELECT 
            (SELECT COUNT(*) FROM produtos WHERE ativo = 1) as total_produtos,
            (SELECT SUM(quantidade) FROM produtos WHERE ativo = 1) as total_itens_estoque,
            (SELECT COUNT(*) FROM movimentacoes WHERE tipo = 'SAIDA') as total_vendas,
            (SELECT COUNT(DISTINCT strftime('%Y-%m-%d', data_movimentacao)) FROM movimentacoes WHERE tipo = 'SAIDA') as dias_com_vendas
        """
        return self.fetchone(query)

    def get_fiados_summary(self):
        """Retorna resumo de fiados: abertos e pagos"""
        query = """
        SELECT
            (SELECT COUNT(*) FROM fiados WHERE pago = 0) as count_open,
            (SELECT COALESCE(SUM(valor_total),0) FROM fiados WHERE pago = 0) as total_open,
            (SELECT COUNT(*) FROM fiados WHERE pago = 1) as count_paid,
            (SELECT COALESCE(SUM(valor_total),0) FROM fiados WHERE pago = 1) as total_paid
        """
        return self.fetchone(query)
