from repositories.base_repository import BaseRepository


class FiadoRepository(BaseRepository):
    """Repositório para operações de fiados"""

    def create(self, cliente_id: int, produto_id: int | None, produto_nome: str | None, quantidade: int, valor_unitario: float, 
               valor_total: float, observacao: str = "", data_vencimento: str = None):
        """Cria um novo fiado para um cliente
        produto_id pode ser None se o produto não existir; nesse caso
        produto_nome deve conter o nome informativo."""
        query = """
        INSERT INTO fiados (
            cliente_id, produto_id, produto_nome, quantidade, valor_unitario, valor_total, 
            valor_pendente, observacao, data_vencimento
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        return self.execute(query, (cliente_id, produto_id, produto_nome, quantidade, valor_unitario, 
                                   valor_total, valor_total, observacao, data_vencimento))

    def get_by_id(self, fiado_id: int):
        """Retorna um fiado pelo ID com informações do cliente e produto"""
        query = """
        SELECT f.id, f.cliente_id, f.produto_id, f.produto_nome, f.quantidade, f.valor_unitario, 
               f.valor_total, f.valor_pendente, f.observacao, f.data_fiado, 
               f.data_vencimento, c.nome as cliente_nome,
               COALESCE(p.nome, f.produto_nome) as produto_nome
        FROM fiados f
        JOIN clientes c ON c.id = f.cliente_id
        LEFT JOIN produtos p ON p.id = f.produto_id
        WHERE f.id = ?
        """
        result = self.fetchone(query, (fiado_id,))
        if result:
            return dict(result)
        return None

    def list_by_cliente(self, cliente_id: int, pendentes=True):
        """Lista fiados de um cliente, opcionalmente apenas os pendentes"""
        query = """
        SELECT f.id, f.cliente_id, f.produto_id, f.produto_nome, f.quantidade, f.valor_unitario, 
               f.valor_total, f.valor_pendente, f.observacao, f.data_fiado, 
               f.data_vencimento, c.nome as cliente_nome,
               COALESCE(p.nome, f.produto_nome) as produto_nome
        FROM fiados f
        JOIN clientes c ON c.id = f.cliente_id
        LEFT JOIN produtos p ON p.id = f.produto_id
        WHERE f.cliente_id = ?
        """
        if pendentes:
            query += " AND f.valor_pendente > 0"
        query += " ORDER BY f.data_fiado DESC"
        results = self.fetchall(query, (cliente_id,))
        return [dict(row) for row in results] if results else []

    def list_open(self):
        """Lista todos os fiados em aberto (com valor pendente > 0)"""
        query = """
        SELECT f.id, f.cliente_id, f.produto_id, f.produto_nome, f.quantidade, f.valor_unitario, 
               f.valor_total, f.valor_pendente, f.observacao, f.data_fiado, 
               f.data_vencimento, c.nome as cliente_nome,
               COALESCE(p.nome, f.produto_nome) as produto_nome
        FROM fiados f
        JOIN clientes c ON c.id = f.cliente_id
        LEFT JOIN produtos p ON p.id = f.produto_id
        WHERE f.valor_pendente > 0
        ORDER BY f.data_fiado DESC
        """
        results = self.fetchall(query)
        return [dict(row) for row in results] if results else []

    def list_by_period(self, start_date: str = None, end_date: str = None):
        """Retorna registros de fiados dentro de um período opcional"""
        query = """
        SELECT f.id, f.cliente_id, f.produto_id, f.produto_nome, f.quantidade, f.valor_unitario, 
               f.valor_total, f.valor_pendente, f.observacao, f.data_fiado, 
               f.data_vencimento, c.nome as cliente_nome,
               COALESCE(p.nome, f.produto_nome) as produto_nome
        FROM fiados f
        JOIN clientes c ON c.id = f.cliente_id
        LEFT JOIN produtos p ON p.id = f.produto_id
        WHERE 1=1
        """
        params = []
        if start_date and end_date:
            query += " AND DATE(f.data_fiado) BETWEEN DATE(?) AND DATE(?)"
            params = [start_date, end_date]

        query += " ORDER BY f.data_fiado DESC"
        results = self.fetchall(query, tuple(params) if params else ())
        return [dict(row) for row in results] if results else []

    def add_pagamento(self, fiado_id: int, valor_pago: float, observacao: str = ""):
        """Adiciona um pagamento parcial a um fiado"""
        # Primeiro, verifica se o fiado existe e pega o valor pendente
        fiado = self.get_by_id(fiado_id)
        if not fiado or fiado['valor_pendente'] <= 0:
            raise ValueError("Fiado não encontrado ou já totalmente pago")

        # Valida se o valor não excede o pendente
        if valor_pago > fiado['valor_pendente']:
            raise ValueError(f"Valor pago ({valor_pago}) não pode exceder o pendente ({fiado['valor_pendente']})")

        # Registra o pagamento
        query = """
        INSERT INTO fiado_pagamentos (fiado_id, valor_pago, observacao)
        VALUES (?, ?, ?)
        """
        pagamento_id = self.execute(query, (fiado_id, valor_pago, observacao))

        # Atualiza o valor pendente no fiado
        novo_pendente = fiado['valor_pendente'] - valor_pago
        self._update_pendente(fiado_id, novo_pendente)

        return pagamento_id

    def _update_pendente(self, fiado_id: int, novo_valor_pendente: float):
        """Atualiza o valor pendente de um fiado (uso interno)"""
        query = """
        UPDATE fiados
        SET valor_pendente = ?
        WHERE id = ?
        """
        self.execute(query, (novo_valor_pendente, fiado_id))

    def get_pagamentos(self, fiado_id: int):
        """Retorna todos os pagamentos de um fiado"""
        query = """
        SELECT id, fiado_id, valor_pago, data_pagamento, observacao
        FROM fiado_pagamentos
        WHERE fiado_id = ?
        ORDER BY data_pagamento DESC
        """
        return self.fetchall(query, (fiado_id,))

    def delete(self, fiado_id: int):
        """Deleta um fiado e seus pagamentos associados"""
        query = """
        DELETE FROM fiado_pagamentos WHERE fiado_id = ?
        """
        self.execute(query, (fiado_id,))
        
        query = """
        DELETE FROM fiados WHERE id = ?
        """
        return self.execute(query, (fiado_id,))

    def get_open_summary(self):
        """Retorna resumo dos fiados em aberto"""
        query = """
        SELECT COUNT(*) as count_open, COALESCE(SUM(valor_pendente), 0) as total_open
        FROM fiados
        WHERE valor_pendente > 0
        """
        result = self.fetchone(query)
        if result:
            return {
                "count_open": result[0],
                "total_open": result[1]
            }
        return {
            "count_open": 0,
            "total_open": 0
        }

    def mark_paid(self, fiado_id: int, movimentacao_id: int = None):
        """Marca um fiado como totalmente pago (valor_pendente = 0)"""
        query = """
        UPDATE fiados
        SET valor_pendente = 0
        WHERE id = ?
        """
        self.execute(query, (fiado_id,))
