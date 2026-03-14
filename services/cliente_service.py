from repositories.cliente_repository import ClienteRepository
from repositories.fiado_repository import FiadoRepository
from repositories.product_repository import ProductRepository
from repositories.caixa_repository import CaixaRepository
from repositories.caixa_movimentacao_repository import CaixaMovimentacaoRepository
from repositories.stock_repository import StockRepository


class ClienteService:
    """Serviço para gerenciar clientes e seus fiados"""

    def __init__(self):
        self.cliente_repo = ClienteRepository()
        self.fiado_repo = FiadoRepository()
        self.produto_repo = ProductRepository()
        self.caixa_repo = CaixaRepository()
        self.caixa_mov_repo = CaixaMovimentacaoRepository()
        self.stock_repo = StockRepository()

    def criar_cliente(self, nome: str, telefone: str = "", email: str = "", endereco: str = ""):
        """Cria um novo cliente"""
        if not nome or not nome.strip():
            raise ValueError("Nome do cliente é obrigatório")

        # Verifica se cliente já existe
        if self.cliente_repo.get_by_name(nome.strip()):
            raise ValueError("Cliente com este nome já existe")

        cliente_id = self.cliente_repo.create(
            nome=nome.strip(),
            telefone=telefone.strip(),
            email=email.strip(),
            endereco=endereco.strip()
        )
        return cliente_id

    def obter_cliente(self, cliente_id: int):
        """Obtém informações de um cliente"""
        return self.cliente_repo.get_by_id(cliente_id)

    def pesquisar_cliente(self, nome: str):
        """Pesquisa clientes por nome (parcial)"""
        if not nome or not nome.strip():
            return []
        return self.cliente_repo.search_by_name(nome.strip())

    def listar_clientes(self):
        """Lista todos os clientes ativos"""
        return self.cliente_repo.list_all()

    def atualizar_cliente(self, cliente_id: int, nome: str, telefone: str = "", 
                         email: str = "", endereco: str = ""):
        """Atualiza dados de um cliente"""
        if not nome or not nome.strip():
            raise ValueError("Nome do cliente é obrigatório")

        self.cliente_repo.update(
            cliente_id,
            nome=nome.strip(),
            telefone=telefone.strip(),
            email=email.strip(),
            endereco=endereco.strip()
        )

    def deletar_cliente(self, cliente_id: int):
        """
        Desativa um cliente (soft delete).
        Se o cliente tiver fiados com valor pendente, volta o estoque dos produtos.
        """
        # Busca todos os fiados incompletos do cliente
        fiados_incompletos = self.fiado_repo.list_by_cliente(cliente_id, pendentes=True)
        
        # Para cada fiado incompleto, volta o estoque do produto
        for fiado in fiados_incompletos:
            # fiado é um dict com: id, cliente_id, produto_id, quantidade, valor_unitario, 
            # valor_total, valor_pendente, observacao, data_fiado, data_vencimento, cliente_nome, produto_nome
            produto_id = fiado['produto_id']
            quantidade = fiado['quantidade']
            
            produto = self.produto_repo.get_by_id(produto_id)
            if produto:
                nova_quantidade = produto['quantidade'] + quantidade
                self.produto_repo.update(
                    produto_id,
                    produto['nome'],
                    nova_quantidade,
                    produto['valor_compra'],
                    produto['valor_venda'],
                    produto['data_validade'],
                    bool(produto['ativo'])
                )
        
        # Após devolver o estoque, faz soft delete do cliente
        self.cliente_repo.delete(cliente_id)

    def criar_fiado(self, cliente_id: int, produto_id: int | None, quantidade: int,
                   produto_nome: str | None = None,
                   observacao: str = "", data_vencimento: str = None):
        """
        Cria um novo fiado para um cliente.
        Se produto_id não é fornecido ou não existe, permite informar um nome livre
        e não altera estoque.
        """
        if quantidade <= 0:
            raise ValueError("Quantidade deve ser maior que zero")

        # Verifica cliente
        cliente = self.cliente_repo.get_by_id(cliente_id)
        if not cliente:
            raise ValueError("Cliente não encontrado")

        valor_unitario = 0.0
        valor_total = 0.0

        if produto_id is not None:
            produto = self.produto_repo.get_by_id(produto_id)
            if produto:
                if produto['quantidade'] < quantidade:
                    raise ValueError("Quantidade insuficiente em estoque")
                valor_unitario = produto['valor_venda']
                valor_total = round(valor_unitario * quantidade, 2)
                # Define produto_nome para o nome do produto registrado
                if produto_nome is None:
                    produto_nome = produto['nome']
                # reduz estoque
                nova_quantidade = produto['quantidade'] - quantidade
                self.produto_repo.update(
                    produto_id,
                    produto['nome'],
                    nova_quantidade,
                    produto['valor_compra'],
                    produto['valor_venda'],
                    produto['data_validade'],
                    bool(produto['ativo'])
                )
                # Registra movimentação de saída
                observacao_mov = f"Fiado criado: {cliente['nome']} - {produto_nome}"
                self.stock_repo.register(produto_id, "SAIDA", quantidade, observacao_mov)
            else:
                # produto_id fornecido mas não existe, ignorar e usar nome livre
                produto_id = None
        # se ainda sem valor e nome fornecido, mantém 0

        fiado_id = self.fiado_repo.create(
            cliente_id=cliente_id,
            produto_id=produto_id,
            produto_nome=produto_nome,
            quantidade=quantidade,
            valor_unitario=valor_unitario,
            valor_total=valor_total,
            observacao=observacao,
            data_vencimento=data_vencimento
        )
        return fiado_id

    def obter_fiado(self, fiado_id: int):
        """Obtém informações de um fiado específico"""
        return self.fiado_repo.get_by_id(fiado_id)

    def listar_fiados_cliente(self, cliente_id: int, pendentes=True):
        """Lista fiados de um cliente"""
        fiados = self.fiado_repo.list_by_cliente(cliente_id, pendentes)
        # Enriquecer com nome do produto se for produto cadastrado
        for fiado in fiados:
            if fiado.get('produto_id') and not fiado.get('produto_nome'):
                produto = self.produto_repo.get_by_id(fiado['produto_id'])
                if produto:
                    fiado['produto_nome'] = produto['nome']
        return fiados

    def listar_fiados_abertos(self):
        """Lista todos os fiados em aberto (com saldo pendente)"""
        return self.fiado_repo.list_open()

    def listar_fiados_periodo(self, start_date: str = None, end_date: str = None):
        """Lista fiados dentro de um período"""
        return self.fiado_repo.list_by_period(start_date, end_date)

    def adicionar_pagamento(self, fiado_id: int, valor_pago: float, observacao: str = ""):
        """
        Adiciona um pagamento parcial a um fiado.
        Registra a entrada no caixa quando o pagamento é feito.
        """
        if valor_pago <= 0:
            raise ValueError("Valor do pagamento deve ser maior que zero")

        fiado = self.fiado_repo.get_by_id(fiado_id)
        if not fiado:
            raise ValueError("Fiado não encontrado")

        if valor_pago > fiado['valor_pendente']:
            raise ValueError(f"Valor pago não pode exceder o pendente (R$ {fiado['valor_pendente']:.2f})")

        # Registra o pagamento no fiado
        pagamento_id = self.fiado_repo.add_pagamento(fiado_id, valor_pago, observacao)

        # Registra ENTRADA no caixa (recebimento do pagamento)
        caixa_hoje = self.caixa_repo.find_today_caixa()
        caixa_id = caixa_hoje['id'] if caixa_hoje else None
        
        cliente_nome = fiado.get('cliente_nome', 'Cliente')
        descricao = f"Pagamento parcial fiado - {cliente_nome}" if observacao else f"Pagamento parcial fiado - {cliente_nome}"
        if observacao:
            descricao += f" ({observacao})"
        
        self.caixa_mov_repo.register(
            caixa_id=caixa_id,
            tipo="ENTRADA",
            valor=valor_pago,
            descricao=descricao,
            categoria="Pagamento de Fiado"
        )

        # Verifica se o fiado foi totalmente pago após este pagamento
        fiado_atualizado = self.fiado_repo.get_by_id(fiado_id)
        if fiado_atualizado and fiado_atualizado['valor_pendente'] == 0:
            # Cria movimentação de SAIDA para contabilizar a venda
            observacao_venda = f"Pagamento completo fiado: {cliente_nome}"
            self.stock_repo.register(fiado['produto_id'], "SAIDA", fiado['quantidade'], observacao_venda)

        return pagamento_id

    def obter_pagamentos_fiado(self, fiado_id: int):
        """Obtém todos os pagamentos de um fiado"""
        return self.fiado_repo.get_pagamentos(fiado_id)

    def deletar_fiado(self, fiado_id: int):
        """Deleta um fiado e seus pagamentos"""
        fiado = self.fiado_repo.get_by_id(fiado_id)
        if not fiado:
            raise ValueError("Fiado não encontrado")

        # Se o fiado ainda tem saldo pendente, recoloca o produto em estoque
        if fiado['valor_pendente'] > 0:
            produto = self.produto_repo.get_by_id(fiado['produto_id'])
            nova_quantidade = produto['quantidade'] + fiado['quantidade']
            self.produto_repo.update(
                fiado['produto_id'],
                produto['nome'],
                nova_quantidade,
                produto['valor_compra'],
                produto['valor_venda'],
                produto['data_validade'],
                bool(produto['ativo'])
            )

        self.fiado_repo.delete(fiado_id)

    def obter_saldo_cliente(self, cliente_id: int):
        """Retorna o saldo pendente total de um cliente"""
        return self.cliente_repo.get_saldo_cliente(cliente_id)

    def obter_resumo_fiados_abertos(self):
        """Retorna resumo dos fiados em aberto"""
        return self.fiado_repo.get_open_summary()
