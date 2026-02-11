from repositories.base_repository import BaseRepository


class PrejuizoRepository(BaseRepository):
    """Repositório para operações de prejuízos"""

    def create(self, produto_id: int, quantidade: int, valor_unitario: float, valor_total: float, motivo: str, observacao: str = ""):
        query = """
        INSERT INTO prejuizos (
            produto_id, quantidade, valor_unitario, valor_total, motivo, observacao
        ) VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.execute(query, (produto_id, quantidade, valor_unitario, valor_total, motivo, observacao))

    def list_by_period(self, start_date: str = None, end_date: str = None):
        query = """
        SELECT p.id, p.produto_id, p.quantidade, p.valor_unitario, p.valor_total, p.motivo, p.observacao, p.data_prejuizo
        FROM prejuizos p
        WHERE 1=1
        """
        params = []
        if start_date and end_date:
            query += " AND DATE(p.data_prejuizo) BETWEEN DATE(?) AND DATE(?)"
            params = [start_date, end_date]

        query += " ORDER BY p.data_prejuizo DESC"
        return self.fetchall(query, tuple(params))

    def summary_by_motivo(self, limit: int = 10):
        query = """
        SELECT motivo, COUNT(*) as count, COALESCE(SUM(valor_total),0) as total
        FROM prejuizos
        GROUP BY motivo
        ORDER BY total DESC
        LIMIT ?
        """
        return self.fetchall(query, (limit,))

    def total_summary(self):
        query = """
        SELECT COUNT(*) as count_total, COALESCE(SUM(valor_total),0) as total_valor
        FROM prejuizos
        """
        return self.fetchone(query)
