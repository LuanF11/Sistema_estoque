from services.tag_service import TagService

class TagController:
    '''
    Controlador responsável por gerenciar as operações relacionadas as tags.
    '''
    def __init__(self):
        self.service = TagService()

    def create_tag(self, nome):
        try:
            self.service.create_tag(nome)
            return {"success": True}
        except ValueError as e:
            return {"success": False, "error": str(e)}
        
    def delete_tag(self, tag_id):
        try:
            self.service.delete_tag(tag_id)
            return {"success": True}
        except ValueError as e:
            return {"success": False, "error": str(e)}
        
    def list_tags(self):
        return self.service.list_tags()
    