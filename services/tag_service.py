from repositories.tag_repository import TagRepository

class TagService:

    '''
    Classe responsável por gerenciar as operações relacionadas às tags.
    '''

    def __init__(self):
        self.tag_repo = TagRepository()

    def create_tag(self, nome: str):
        if not nome:
            raise ValueError("O nome da tag é obrigatório.")
        
        if self.tag_repo.get_by_name(nome):
            raise ValueError("Já existe uma tag com esse nome.")
        
        self.tag_repo.create(nome)
    
    def delete_tag(self, tag_id: int):
        self.tag_repo.delete(tag_id)

    def list_tags(self):
        return self.tag_repo.list_all()