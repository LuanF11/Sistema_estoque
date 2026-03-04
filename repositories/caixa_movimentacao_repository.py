from repositories.base_repository import BaseRepository
from datetime import date


class CaixaMovimentacaoRepository(BaseRepository):

    def register(self, caixa_id: int | None, tipo: str, valor: float, descricao: str = "", categoria: str | None = None):
        query = """
            INSERT INTO caixa_movimentacoes (
                caixa_id,
                tipo,
                valor,
                categoria,
                descricao
            ) VALUES (?, ?, ?, ?, ?)
        """
        params = (caixa_id, tipo, valor, categoria, descricao)
        return self.execute(query, params)

    def sum_by_date(self, target_date: str, tipo: str | None = None):
        """Soma os valores de movimentações para uma data. Se tipo passado, filtra por ENTRADA/SAIDA."""
        if tipo:
            query = """
                SELECT IFNULL(SUM(valor), 0) FROM caixa_movimentacoes
                WHERE DATE(data_movimentacao) = DATE(?) AND tipo = ?
            """
            return self.fetchone(query, (target_date, tipo))[0]
        else:
            query = """
                SELECT IFNULL(SUM(valor), 0) FROM caixa_movimentacoes
                WHERE DATE(data_movimentacao) = DATE(?)
            """
            return self.fetchone(query, (target_date,))[0]

    def list_by_date(self, target_date: str):
        query = """
            SELECT * FROM caixa_movimentacoes
            WHERE DATE(data_movimentacao) = DATE(?)
            ORDER BY data_movimentacao
        """
        return self.fetchall(query, (target_date,))
