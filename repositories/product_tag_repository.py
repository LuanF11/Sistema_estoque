from repositories.base_repository import BaseRepository

class ProductTagRepository(BaseRepository):

    '''
    Classe de repositório para gerenciar operações de banco de dados relacionadas à associação entre produtos e tags.
    '''

    def add_tag_to_product(self, produto_id: int, tag_id: int):
        query = "INSERT OR IGNORE INTO produto_tag (produto_id, tag_id) VALUES (?, ?)"
        self.execute(query, (produto_id, tag_id))
    
    def remove_tag_from_product(self, produto_id: int, tag_id: int):
        query = "DELETE FROM produto_tag WHERE produto_id = ? AND tag_id = ?"
        self.execute(query, (produto_id, tag_id))

    def get_tags_by_product(self, produto_id: int):
        query = """
        SELECT t.*
        FROM tags t
        JOIN produto_tag pt ON pt.tag_id = t.id
        WHERE pt.produto_id = ?
        ORDER BY t.nome
        """
        return self.fetchall(query, (produto_id,))
    
    def get_products_by_tag(self, tag_id: int):
        query = """
        SELECT p.*
        FROM produtos p
        JOIN produto_tag pt ON pt.produto_id = p.id
        WHERE pt.tag_id = ?
        AND p.ativo = 1
        ORDER BY p.nome
        """
        return self.fetchall(query, (tag_id,))