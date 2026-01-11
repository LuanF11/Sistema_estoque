from repositories.product_repository import ProductRepository
from repositories.stock_repository import StockRepository


class StockService:
    """
    Classe responsável por gerenciar as operações relacionadas ao estoque.
    """

    def __init__(self):
        self.product_repo = ProductRepository()
        self.stock_repo = StockRepository()

    def entrada_produto(
        self,
        produto_id: int,
        quantidade: int,
        observacao: str = ""
    ):
        if quantidade <= 0:
            raise ValueError("A quantidade de entrada deve ser maior que zero.")

        produto = self.product_repo.get_by_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado.")

        nova_quantidade = produto["quantidade"] + quantidade

        # Atualiza o estoque do produto
        self.product_repo.update(
            produto_id,
            produto["nome"],
            nova_quantidade,
            produto["valor_compra"],
            produto["valor_venda"],
            produto["data_validade"],
            bool(produto["ativo"])
        )

        # Registra movimentação (SEM valor_unitario)
        self.stock_repo.register(
            produto_id,
            "ENTRADA",
            quantidade,
            observacao
        )

    def saida_produto(
        self,
        produto_id: int,
        quantidade: int,
        observacao: str = ""
    ):
        if quantidade <= 0:
            raise ValueError("A quantidade de saída deve ser maior que zero.")

        produto = self.product_repo.get_by_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado.")

        if produto["quantidade"] < quantidade:
            raise ValueError("Quantidade insuficiente em estoque para a saída.")

        nova_quantidade = produto["quantidade"] - quantidade

        # Atualiza o estoque do produto
        self.product_repo.update(
            produto_id,
            produto["nome"],
            nova_quantidade,
            produto["valor_compra"],
            produto["valor_venda"],
            produto["data_validade"],
            bool(produto["ativo"])
        )

        # Registra movimentação (SEM valor_unitario)
        self.stock_repo.register(
            produto_id,
            "SAIDA",
            quantidade,
            observacao
        )
