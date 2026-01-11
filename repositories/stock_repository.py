from repositories.base_repository import BaseRepository


class StockRepository(BaseRepository):

    def register(
        self,
        produto_id: int,
        tipo: str,
        quantidade: int,
        observacao: str = "",
    ):
        """
        Registra uma movimentação de estoque (ENTRADA ou SAIDA).
        A data é registrada automaticamente pelo SQLite.
        """
        query = """
            INSERT INTO movimentacoes (
                produto_id,
                tipo,
                quantidade,
                observacao
            )
            VALUES (?, ?, ?, ?)
        """
        self.execute(query, (produto_id, tipo, quantidade, observacao))

    def list_by_period(self, data_inicio: str, data_fim: str):
        """
        Lista movimentações dentro de um período de datas.
        """
        query = """
            SELECT *
            FROM movimentacoes
            WHERE DATE(data_movimentacao)
                  BETWEEN DATE(?) AND DATE(?)
            ORDER BY data_movimentacao
        """
        return self.fetchall(query, (data_inicio, data_fim))
