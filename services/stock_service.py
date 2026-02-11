from repositories.product_repository import ProductRepository
from repositories.stock_repository import StockRepository
from repositories.fiado_repository import FiadoRepository
from repositories.prejuizo_repository import PrejuizoRepository


class StockService:
    """
    Classe responsável por gerenciar as operações relacionadas ao estoque.
    """

    def __init__(self):
        self.product_repo = ProductRepository()
        self.stock_repo = StockRepository()
        self.fiado_repo = FiadoRepository()
        self.prejuizo_repo = PrejuizoRepository()

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
        observacao: str = "",
        fiado: bool = False,
        cliente: str | None = None
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

        # Se for fiado, cria registro em fiados e não registra movimentação ainda
        if fiado:
            if not cliente or not cliente.strip():
                raise ValueError("Nome do cliente é obrigatório para fiado.")

            valor_unitario = produto["valor_venda"]
            valor_total = round(valor_unitario * quantidade, 2)

            self.fiado_repo.create(
                produto_id=produto_id,
                quantidade=quantidade,
                valor_unitario=valor_unitario,
                valor_total=valor_total,
                cliente=cliente.strip()
            )
        else:
            # Registra movimentação (SEM valor_unitario)
            self.stock_repo.register(
                produto_id,
                "SAIDA",
                quantidade,
                observacao
            )

    def list_open_fiados(self):
        """Retorna lista de fiados em aberto."""
        return self.fiado_repo.list_open()

    def register_prejuizo(self, produto_id: int, quantidade: int, motivo: str, observacao: str = ""):
        """Registra um prejuízo: reduz estoque e grava registro de prejuizo."""
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero.")

        produto = self.product_repo.get_by_id(produto_id)
        if not produto:
            raise ValueError("Produto não encontrado.")

        if produto["quantidade"] < quantidade:
            raise ValueError("Quantidade insuficiente em estoque para registrar prejuízo.")

        nova_quantidade = produto["quantidade"] - quantidade

        # Atualiza estoque
        self.product_repo.update(
            produto_id,
            produto["nome"],
            nova_quantidade,
            produto["valor_compra"],
            produto["valor_venda"],
            produto["data_validade"],
            bool(produto["ativo"])
        )

        valor_unitario = produto["valor_venda"]
        valor_total = round(valor_unitario * quantidade, 2)

        prej_id = self.prejuizo_repo.create(
            produto_id=produto_id,
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            motivo=motivo,
            observacao=observacao
        )

        return prej_id

    def pay_fiado(self, fiado_id: int):
        """Marca fiado como pago: cria movimentação SAIDA (para contabilizar nas vendas) e atualiza registro de fiado."""
        # Busca fiado
        # (repository.list_open() returns rows but we need the fiado data to create movimentacao)
        open_fiados = self.fiado_repo.list_open()
        target = None
        for f in open_fiados:
            if f[0] == fiado_id:
                target = f
                break

        if not target:
            raise ValueError("Fiado não encontrado ou já pago")

        # target: (id, produto_id, quantidade, valor_unitario, valor_total, cliente, data_fiado)
        produto_id = target[1]
        quantidade = target[2]
        observacao = f"Pagamento fiado: {target[5]}"

        # Cria movimentação de SAIDA para contabilizar a venda
        movimentacao_id = self.stock_repo.register(produto_id, "SAIDA", quantidade, observacao)

        # Marca fiado como pago e vincula a movimentação
        self.fiado_repo.mark_paid(fiado_id, movimentacao_id)
