from services.cliente_service import ClienteService


class ClienteController:
    """Controller para operações com clientes"""

    def __init__(self):
        self.service = ClienteService()

    def criar_cliente(self, nome: str, telefone: str = "", email: str = "", endereco: str = ""):
        """Cria um novo cliente"""
        try:
            cliente_id = self.service.criar_cliente(nome, telefone, email, endereco)
            return {"success": True, "cliente_id": cliente_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def obter_cliente(self, cliente_id: int):
        """Obtém informações de um cliente"""
        try:
            cliente = self.service.obter_cliente(cliente_id)
            return {"success": True, "cliente": cliente}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def pesquisar_cliente(self, nome: str):
        """Pesquisa clientes por nome"""
        try:
            clientes = self.service.pesquisar_cliente(nome)
            return {"success": True, "clientes": clientes}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def listar_clientes(self):
        """Lista todos os clientes"""
        try:
            clientes = self.service.listar_clientes()
            return {"success": True, "clientes": clientes}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def atualizar_cliente(self, cliente_id: int, nome: str, telefone: str = "", 
                         email: str = "", endereco: str = ""):
        """Atualiza dados de um cliente"""
        try:
            self.service.atualizar_cliente(cliente_id, nome, telefone, email, endereco)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def deletar_cliente(self, cliente_id: int):
        """Deleta um cliente"""
        try:
            self.service.deletar_cliente(cliente_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def criar_fiado(self, cliente_id: int, produto_id: int | None, quantidade: int,
                   produto_nome: str | None = None,
                   observacao: str = "", data_vencimento: str = None):
        """Cria um novo fiado para um cliente"""
        try:
            fiado_id = self.service.criar_fiado(cliente_id, produto_id, quantidade,
                                               produto_nome, observacao, data_vencimento)
            return {"success": True, "fiado_id": fiado_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def obter_fiado(self, fiado_id: int):
        """Obtém informações de um fiado"""
        try:
            fiado = self.service.obter_fiado(fiado_id)
            return {"success": True, "fiado": fiado}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def listar_fiados_cliente(self, cliente_id: int, pendentes=True):
        """Lista fiados de um cliente"""
        try:
            fiados = self.service.listar_fiados_cliente(cliente_id, pendentes)
            return {"success": True, "fiados": fiados}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def listar_fiados_abertos(self):
        """Lista todos os fiados em aberto"""
        try:
            fiados = self.service.listar_fiados_abertos()
            return {"success": True, "fiados": fiados}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def listar_fiados_periodo(self, start_date: str = None, end_date: str = None):
        """Lista fiados dentro de um período"""
        try:
            fiados = self.service.listar_fiados_periodo(start_date, end_date)
            return {"success": True, "fiados": fiados}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def adicionar_pagamento(self, fiado_id: int, valor_pago: float, observacao: str = ""):
        """Adiciona um pagamento parcial a um fiado"""
        try:
            pagamento_id = self.service.adicionar_pagamento(fiado_id, valor_pago, observacao)
            return {"success": True, "pagamento_id": pagamento_id}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def obter_pagamentos_fiado(self, fiado_id: int):
        """Obtém os pagamentos de um fiado"""
        try:
            pagamentos = self.service.obter_pagamentos_fiado(fiado_id)
            return {"success": True, "pagamentos": pagamentos}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def deletar_fiado(self, fiado_id: int):
        """Deleta um fiado"""
        try:
            self.service.deletar_fiado(fiado_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def obter_saldo_cliente(self, cliente_id: int):
        """Obtém o saldo pendente de um cliente"""
        try:
            saldo = self.service.obter_saldo_cliente(cliente_id)
            return {"success": True, "saldo": saldo}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def obter_resumo_fiados_abertos(self):
        """Obtém resumo dos fiados em aberto"""
        try:
            resumo = self.service.obter_resumo_fiados_abertos()
            return {"success": True, "resumo": resumo}
        except Exception as e:
            return {"success": False, "error": str(e)}
