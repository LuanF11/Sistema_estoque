from repositories.base_repository import BaseRepository

class StockRepository(BaseRepository):

    def register(
            self,
            produto_id: int,
            tipo:str,
            quantidade:int,
            valor_unitario:float,
            observacao: str = "",
    ):
        query = "INSERT INTO movimentacoes(produto_id, tipo, quantidade, valor_unitario, observacao) VALUES (?, ?, ?, ?, ?)"
        self.execute(query, (produto_id, tipo, quantidade, valor_unitario, observacao))
    
    def list_by_period(self, data_inicio: str, data_fim: str):
        query = "SELECT * FROM movimentacoes WHERE DATE(data_movimentacao) BETWEEN DATE(?) AND DATE(?) ORDER BY data_movimentacao"
        return self.fetchall(query, (data_inicio, data_fim))