from datetime import date, datetime
from typing import Optional
from repositories.product_repository import ProductRepository
from repositories.product_tag_repository import ProductTagRepository

class ProductService:

    '''
    Classe responsável por gerenciar as operações relacionadas aos produtos.
    '''

    def __init__(self):
        self.product_repo = ProductRepository()
        self.product_tag_repo = ProductTagRepository()

    def create_product(
            self,
            nome:str,
            quantidade:int,
            valor_compra:float,
            valor_venda:float,
            data_validade: Optional[date],
            tag_ids: list[int] = [],
            estoque_minimo: int = 5

    ):
        if not nome:
            raise ValueError("O nome do produto é obrigatório.")
        
        if quantidade < 0:
            raise ValueError("A quantidade do produto não pode ser negativa.")
        
        if valor_compra < 0 or valor_venda < 0:
            raise ValueError("Os valores de compra e venda não podem ser negativos.")
        
        if estoque_minimo < 0:
            raise ValueError("O estoque mínimo não pode ser negativo.")
        
        self.product_repo.create(nome, quantidade, valor_compra, valor_venda, data_validade, estoque_minimo)
        produto = self.product_repo.search_by_name(nome)[-1]  # Pega o último produto inserido com esse nome

        for tag_id in tag_ids:
            self.product_tag_repo.add_tag_to_product(produto["id"], tag_id)
    
    def update_product(
            self,
            produto_id: int,
            nome:str,
            quantidade:int,
            valor_compra:float,
            valor_venda:float,
            data_validade: Optional[date],
            ativo: bool,
            tag_ids: list[int],
            estoque_minimo: int = 5
    ):
        self.product_repo.update(produto_id, nome, quantidade, valor_compra, valor_venda, data_validade, ativo, estoque_minimo)
        existing_tags = self.product_tag_repo.get_tags_by_product(produto_id)

        for tag_id in existing_tags:
            self.product_tag_repo.remove_tag_from_product(produto_id, tag_id["id"])

        for tag_id in tag_ids:
            self.product_tag_repo.add_tag_to_product(produto_id, tag_id)

    def list_products(self):
        return self.product_repo.list_all()
    
    def search_products_by_name(self, nome: str):
        return self.product_repo.search_by_name(nome)
    
    def get_products_near_expiration(self, days: int):
        return self.product_repo.products_near_expiry(days)
    
    def search_products_by_name_or_tag(self, termo: str):
        if not termo:
            return self.product_repo.list_all()
        return self.product_repo.search_by_name_or_tag(termo)
    
    def get_product_alert_status(self, product: dict, warning_days: int = 7):
        """
        Retorna uma lista com todos os alertas aplicáveis ao produto.
        Pode conter: 'Vencido', 'Perto do vencimento', 'Estoque baixo'
        """
        alertas = []
        
        # Verificar estoque mínimo
        estoque_minimo = product.get("estoque_minimo", 5)
        quantidade = product.get("quantidade", 0)
        
        if quantidade < estoque_minimo:
            alertas.append("Estoque baixo")
        
        # Verificar validade
        validade = product.get("data_validade")
        if validade:
            validade_date = datetime.strptime(validade, "%Y-%m-%d").date()
            today = date.today()

            if validade_date < today:
                alertas.append("Vencido")
            elif (validade_date - today).days <= warning_days:
                alertas.append("Perto do vencimento")

        return alertas
