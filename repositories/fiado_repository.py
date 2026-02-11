from repositories.base_repository import BaseRepository


class FiadoRepository(BaseRepository):
    """Repositório para operações de fiados"""

    def create(self, produto_id: int, quantidade: int, valor_unitario: float, valor_total: float, cliente: str):
        query = """
        INSERT INTO fiados (
            produto_id, quantidade, valor_unitario, valor_total, cliente
        ) VALUES (?, ?, ?, ?, ?)
        """
        return self.execute(query, (produto_id, quantidade, valor_unitario, valor_total, cliente))

    def list_open(self):
        query = """
        SELECT f.id, f.produto_id, f.quantidade, f.valor_unitario, f.valor_total, f.cliente, f.data_fiado
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

    def get_open_summary(self):
        query = """
        SELECT COUNT(*) as count_open, COALESCE(SUM(valor_total),0) as total_open
        FROM fiados
        WHERE pago = 0
        """
        return self.fetchone(query)
