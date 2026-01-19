from services.product_service import ProductService

class ProductController:
    '''
    Controlador responsável por gerenciar as operações relacionadas aos produtos.
    '''

    def __init__(self):
        self.service = ProductService()

    def create_product(
            self,
            nome,
            quantidade,
            valor_compra,
            valor_venda,
            data_validade,
            tag_ids,
            estoque_minimo
    ):
    
        try:
            self.service.create_product(
                nome,
                quantidade,
                valor_compra,
                valor_venda,
                data_validade,
                tag_ids,
                estoque_minimo
            )
            return {"success": True}
        except ValueError as e:
            return {"success": False, "error": str(e)}
        
    def update_product(
            self,
            produto_id,
            nome,
            quantidade,
            valor_compra,
            valor_venda,
            data_validade,
            ativo,
            tag_ids,
            estoque_minimo
    ):
        try:
            self.service.update_product(
                produto_id,
                nome,
                quantidade,
                valor_compra,
                valor_venda,
                data_validade,
                ativo,
                tag_ids,
                estoque_minimo
            )
            return {"success": True}
        except ValueError as e:
            return {"success": False, "error": str(e)}
        
    def list_products(self):
        return self.service.list_products()
    
    def search_by_name(self, nome):
        return self.service.search_products_by_name(nome)
    
    def products_near_expiration(self, days):
        return self.service.get_products_near_expiration(days)
    
    def get_tags_by_product(self, produto_id):
        return self.service.product_tag_repo.get_tags_by_product(produto_id)
    
    def search_by_name_or_tag(self, termo):
        return self.service.search_products_by_name_or_tag(termo)

