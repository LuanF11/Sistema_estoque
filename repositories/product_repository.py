from datetime import date
from typing import Optional
from repositories.base_repository import BaseRepository

class ProductRepository(BaseRepository):

    '''
    Classe de repositório para gerenciar operações de banco de dados relacionadas a produtos.
    '''

    def create(
            self,
            nome:str,
            quantidade:int,
            valor_compra:float,
            valor_venda:float,
            data_validade: Optional[date],
    ):
        query = """
        INSERT INTO produtos (nome, quantidade, valor_compra, valor_venda, data_validade)
        VALUES (?, ?, ?, ?, ?)
        """
        self.execute(query, (nome, quantidade, valor_compra, valor_venda, data_validade))
    
    def update(
            self,
            product_id: int,
            nome:str,
            quantidade:int,
            valor_compra:float,
            valor_venda:float,
            data_validade: Optional[date],
            ativo: bool,
    ):
        query = """
        UPDATE produtos
        SET nome = ?, quantidade = ?, valor_compra = ?, valor_venda = ?, data_validade = ?, ativo = ?
        WHERE id = ?
        """
        self.execute(query, (nome, quantidade, valor_compra, valor_venda, data_validade, int(ativo), product_id))
    
    def delete(self, product_id: int):
        query = "DELETE FROM produtos WHERE id = ?"
        self.execute(query, (product_id,))
    
    def get_by_id(self, product_id: int):
        query = "SELECT * FROM produtos WHERE id = ?"
        return self.fetchone(query, (product_id,))
    
    def list_all(self, only_active: bool = True):
        if only_active:
            query = "SELECT * FROM produtos WHERE ativo = 1 = ORDER BY nome"
            return self.fetchall(query)
        else:
            query = "SELECT * FROM produtos ORDER BY nome"
            return self.fetchall(query)
    
    def search_by_name(self, nome: str):
        query = "SELECT * FROM produtos WHERE nome LIKE ? ORDER BY nome"
        return self.fetchall(query, (f"%{nome}%",))
    
    def products_near_expiry(self, days: int):
        query = """
        SELECT * FROM produtos
        WHERE data_validade IS NOT NULL
        AND DATE(data_validade) <= DATE('now', ? || ' days')
        AND ativo = 1
        ORDER BY data_validade
        """
        return self.fetchall(query, (days,))