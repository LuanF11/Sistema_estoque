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
        query = """
        SELECT 
            p.id,
            p.nome,
            p.quantidade,
            p.valor_compra,
            p.valor_venda,
            p.data_validade,
            p.ativo,
            GROUP_CONCAT(t.nome, ', ') AS tags
        FROM produtos p
        LEFT JOIN produto_tag pt ON pt.produto_id = p.id
        LEFT JOIN tags t ON t.id = pt.tag_id
        """

        params = ()

        if only_active:
            query += " WHERE p.ativo = 1"

        query += """
        GROUP BY p.id
        ORDER BY p.nome
        """

        rows = self.fetchall(query, params)

        return [
            {
                "id": row["id"],
                "nome": row["nome"],
                "quantidade": row["quantidade"],
                "valor_compra": row["valor_compra"],
                "valor_venda": row["valor_venda"],
                "data_validade": row["data_validade"],
                "ativo": row["ativo"],
                "tags": row["tags"] or ""
            }
            for row in rows
        ]
    # def list_all(self, only_active: bool = True):
    #     if only_active:
    #         query = "SELECT * FROM produtos WHERE ativo = 1 ORDER BY nome"
    #         return self.fetchall(query)
    #     else:
    #         query = "SELECT * FROM produtos ORDER BY nome"
    #         return self.fetchall(query)
    
    # def search_by_name(self, nome: str):
    #     query = "SELECT * FROM produtos WHERE nome LIKE ? ORDER BY nome"
    #     return self.fetchall(query, (f"%{nome}%",))

    def search_by_name(self, nome: str):
        query = """
        SELECT 
            p.id,
            p.nome,
            p.quantidade,
            p.valor_compra,
            p.valor_venda,
            p.data_validade,
            p.ativo,
            GROUP_CONCAT(t.nome, ', ') AS tags
        FROM produtos p
        LEFT JOIN produto_tag pt ON pt.produto_id = p.id
        LEFT JOIN tags t ON t.id = pt.tag_id
        WHERE p.nome LIKE ?
        GROUP BY p.id
        ORDER BY p.nome
        """

        rows = self.fetchall(query, (f"%{nome}%",))

        return [
            {
                "id": row["id"],
                "nome": row["nome"],
                "quantidade": row["quantidade"],
                "valor_compra": row["valor_compra"],
                "valor_venda": row["valor_venda"],
                "data_validade": row["data_validade"],
                "ativo": row["ativo"],
                "tags": row["tags"] or ""
            }
            for row in rows
        ]

    
    def products_near_expiry(self, days: int):
        query = """
        SELECT * FROM produtos
        WHERE data_validade IS NOT NULL
        AND DATE(data_validade) <= DATE('now', ? || ' days')
        AND ativo = 1
        ORDER BY data_validade
        """
        return self.fetchall(query, (days,))
    
    # def search_by_name_or_tag(self, termo: str):
    #     query = """
    #     SELECT DISTINCT p.*
    #     FROM produtos p
    #     LEFT JOIN produto_tag pt ON pt.produto_id = p.id
    #     LEFT JOIN tags t ON t.id = pt.tag_id
    #     WHERE p.nome LIKE ?
    #     OR t.nome LIKE ?
    #     AND p.ativo = 1
    #     ORDER BY p.nome
    #     """
    #     like = f"%{termo}%"
    #     return self.fetchall(query, (like, like))

    def search_by_name_or_tag(self, termo: str):
        query = """
        SELECT 
            p.id,
            p.nome,
            p.quantidade,
            p.valor_compra,
            p.valor_venda,
            p.data_validade,
            p.ativo,
            GROUP_CONCAT(t.nome, ', ') AS tags
        FROM produtos p
        LEFT JOIN produto_tag pt ON pt.produto_id = p.id
        LEFT JOIN tags t ON t.id = pt.tag_id
        WHERE p.id IN (
            SELECT p2.id
            FROM produtos p2
            LEFT JOIN produto_tag pt2 ON pt2.produto_id = p2.id
            LEFT JOIN tags t2 ON t2.id = pt2.tag_id
            WHERE p2.nome LIKE ?
            OR t2.nome LIKE ?
        )
        AND p.ativo = 1
        GROUP BY p.id
        ORDER BY p.nome
        """
        like = f"%{termo}%"
        rows = self.fetchall(query, (like, like))

        return [
            {
                "id": row["id"],
                "nome": row["nome"],
                "quantidade": row["quantidade"],
                "valor_compra": row["valor_compra"],
                "valor_venda": row["valor_venda"],
                "data_validade": row["data_validade"],
                "ativo": row["ativo"],
                "tags": row["tags"] or ""
            }
            for row in rows
        ]
    
