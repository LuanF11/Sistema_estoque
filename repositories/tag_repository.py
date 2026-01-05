from repositories.base_repository import BaseRepository

class TagRepository(BaseRepository):

    '''
    Classe de repositório para gerenciar operações de banco de dados relacionadas a tags.
    '''
    
    def create(self, nome: str):
        query = "INSERT INTO tags (nome) VALUES (?)"
        self.execute(query, (nome,))

    def delete(self, tag_id: int):
        query = "DELETE FROM tags WHERE id = ?"
        self.execute(query, (tag_id,))

    def list_all(self):
        query = "SELECT * FROM tags ORDER BY nome"
        return self.fetchall(query)
    
    def get_by_name(self, nome: str):
        query = "SELECT * FROM tags WHERE nome = ?"
        return self.fetchone(query, (nome,))