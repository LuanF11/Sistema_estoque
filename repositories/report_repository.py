from repositories.base_repository import BaseRepository


class ReportRepository(BaseRepository):

    def get_sales_summary(self, start_date, end_date):
        query = """
        SELECT
            p.id,
            p.nome,
            SUM(m.quantidade) AS total_vendido,
            SUM(m.quantidade * p.valor_venda) AS faturamento,
            SUM(m.quantidade * (p.valor_venda - p.valor_compra)) AS lucro_estimado
        FROM movimentacoes m
        JOIN produtos p ON p.id = m.produto_id
        WHERE m.tipo = 'SAIDA'
          AND DATE(m.data_movimentacao) BETWEEN DATE(?) AND DATE(?)
        GROUP BY p.id, p.nome
        ORDER BY total_vendido DESC
        """
        return self.fetchall(query, (start_date, end_date))
