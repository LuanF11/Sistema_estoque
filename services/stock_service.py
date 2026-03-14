from repositories.product_repository import ProductRepository
from repositories.stock_repository import StockRepository
from repositories.fiado_repository import FiadoRepository
from repositories.prejuizo_repository import PrejuizoRepository
from repositories.caixa_repository import CaixaRepository
from repositories.caixa_movimentacao_repository import CaixaMovimentacaoRepository


class StockService:
    """
    Classe responsável por gerenciar as operações relacionadas ao estoque.
    """

    def __init__(self):
        self.product_repo = ProductRepository()
        self.stock_repo = StockRepository()
        self.fiado_repo = FiadoRepository()
        self.prejuizo_repo = PrejuizoRepository()
        self.caixa_repo = CaixaRepository()
        self.caixa_mov_repo = CaixaMovimentacaoRepository()

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
                cliente=cliente.strip(),
                observacao=observacao
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

    def remove_prejuizo(self, prejuizo_id: int):
        """Remove um prejuízo previamente registrado e repõe o estoque do produto.

        A exclusão apenas é permitida se o prejuízo existir. O estoque é ajustado
        adicionando-se novamente a quantidade perdida.
        """
        # Busca registro existente
        prej = self.prejuizo_repo.get_by_id(prejuizo_id)
        if not prej:
            raise ValueError("Prejuízo não encontrado.")

        produto_id = prej[1]  # tuple: (id, produto_id, quantidade, ...)
        quantidade = prej[2]

        # Atualiza estoque adicionando a quantidade do prejuízo
        produto = self.product_repo.get_by_id(produto_id)
        if not produto:
            raise ValueError("Produto associado ao prejuízo não encontrado.")

        nova_quantidade = produto["quantidade"] + quantidade
        self.product_repo.update(
            produto_id,
            produto["nome"],
            nova_quantidade,
            produto["valor_compra"],
            produto["valor_venda"],
            produto["data_validade"],
            bool(produto["ativo"])
        )

        # por fim, exclui o registro de prejuízo
        self.prejuizo_repo.delete(prejuizo_id)

    def pay_fiado(self, fiado_id: int):
        """
        Marca fiado como pago: 
        1. Registra movimentação de SAIDA (para contabilizar nas vendas)
        2. Registra movimento de ENTRADA no caixa (recebimento do pagamento)
        3. Atualiza registro de fiado
        """
        # Busca fiado por ID
        fiado = self.fiado_repo.get_by_id(fiado_id)
        if not fiado:
            raise ValueError("Fiado não encontrado")

        # Extrai dados do fiado
        # get_by_id retorna dict com chaves: id, cliente_id, produto_id, quantidade, valor_unitario, 
        # valor_total, valor_pendente, observacao, data_fiado, data_vencimento, cliente_nome, produto_nome
        produto_id = fiado['produto_id']
        quantidade = fiado['quantidade']
        valor_total = fiado['valor_total']
        cliente_nome = fiado.get('cliente_nome', 'Cliente')
        observacao = f"Pagamento fiado: {cliente_nome}"

        # Cria movimentação de SAIDA para contabilizar a venda no histórico de estoque
        movimentacao_id = self.stock_repo.register(produto_id, "SAIDA", quantidade, observacao)

        # Registra ENTRADA no caixa (recebimento do pagamento do fiado)
        caixa_hoje = self.caixa_repo.find_today_caixa()
        caixa_id = caixa_hoje['id'] if caixa_hoje else None
        
        self.caixa_mov_repo.register(
            caixa_id=caixa_id,
            tipo="ENTRADA",
            valor=valor_total,
            descricao=observacao,
            categoria="Pagamento de Fiado"
        )

        # Marca fiado como pago
        self.fiado_repo.mark_paid(fiado_id, movimentacao_id)

    def remove_fiado(self, fiado_id: int):
        """Exclui um fiado em aberto e repõe o estoque."""
        fiado = self.fiado_repo.get_by_id(fiado_id)
        if not fiado:
            raise ValueError("Fiado não encontrado.")

        pago = fiado[6] == 0  # valor_pendente == 0 significa pago
        if pago:
            raise ValueError("Não é possível excluir um fiado já pago.")

        produto_id = fiado[1]
        quantidade = fiado[2]

        # Ajusta estoque devolvendo quantidade vendida
        produto = self.product_repo.get_by_id(produto_id)
        if not produto:
            raise ValueError("Produto associado ao fiado não encontrado.")

        nova_quantidade = produto["quantidade"] + quantidade
        self.product_repo.update(
            produto_id,
            produto["nome"],
            nova_quantidade,
            produto["valor_compra"],
            produto["valor_venda"],
            produto["data_validade"],
            bool(produto["ativo"])
        )

        # Exclui o registro do fiado
        self.fiado_repo.delete(fiado_id)
