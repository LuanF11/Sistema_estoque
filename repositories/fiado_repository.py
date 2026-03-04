from repositories.base_repository import BaseRepository


class FiadoRepository(BaseRepository):
    """Repositório para operações de fiados"""

    def create(self, produto_id: int, quantidade: int, valor_unitario: float, valor_total: float, cliente: str, observacao: str = ""):
        query = """
        INSERT INTO fiados (
            produto_id, quantidade, valor_unitario, valor_total, cliente, observacao
        ) VALUES (?, ?, ?, ?, ?, ?)
        """
        return self.execute(query, (produto_id, quantidade, valor_unitario, valor_total, cliente, observacao))

    def list_open(self):
        query = """
        SELECT f.id, f.produto_id, f.quantidade, f.valor_unitario, f.valor_total, f.cliente, f.observacao, f.data_fiado
        FROM fiados f
        WHERE f.pago = 0
        ORDER BY f.data_fiado DESC
        """
        return self.fetchall(query)

    def mark_paid(self, fiado_id: int, movimentacao_id: int | None = None):
        query = """
        UPDATE fiados
        SET pago = 1,
            data_pagamento = CURRENT_TIMESTAMP,
            movimentacao_id = ?
        WHERE id = ?
        """
        self.execute(query, (movimentacao_id, fiado_id))

    def get_by_id(self, fiado_id: int):
        query = """
        SELECT id, produto_id, quantidade, valor_unitario, valor_total,
               cliente, observacao, data_fiado, pago
        FROM fiados
        WHERE id = ?
        """
        return self.fetchone(query, (fiado_id,))

    def delete(self, fiado_id: int):
        query = """
        DELETE FROM fiados WHERE id = ?
        """
        return self.execute(query, (fiado_id,))

    def list_by_period(self, start_date: str = None, end_date: str = None):
        """Retorna registros de fiados (abertos e pagos) dentro de um período opcional.

        Os dados já vêm com nome do produto para facilitar exibição.
        """
        query = """
        SELECT f.id, f.produto_id, p.nome as produto_nome,
               f.quantidade, f.valor_unitario, f.valor_total,
               f.cliente, f.observacao, f.pago, f.data_fiado, f.data_pagamento
        FROM fiados f
        JOIN produtos p ON p.id = f.produto_id
        WHERE 1=1
        """
        params = []
        if start_date and end_date:
            query += " AND DATE(f.data_fiado) BETWEEN DATE(?) AND DATE(?)"
            params = [start_date, end_date]

        query += " ORDER BY f.data_fiado DESC"
        return self.fetchall(query, tuple(params) if params else ())

    def get_open_summary(self):
        query = """
        SELECT COUNT(*) as count_open, COALESCE(SUM(valor_total),0) as total_open
        FROM fiados
        WHERE pago = 0
        """
        return self.fetchone(query)
