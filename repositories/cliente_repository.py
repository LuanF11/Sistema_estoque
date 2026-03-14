from repositories.base_repository import BaseRepository


class ClienteRepository(BaseRepository):
    """Repositório para operações com clientes"""

    def create(self, nome: str, telefone: str = "", email: str = "", endereco: str = ""):
        """Cria um novo cliente"""
        query = """
        INSERT INTO clientes (nome, telefone, email, endereco)
        VALUES (?, ?, ?, ?)
        """
        return self.execute(query, (nome, telefone, email, endereco))

    def get_by_id(self, cliente_id: int):
        """Retorna um cliente por ID"""
        query = """
        SELECT id, nome, telefone, email, endereco, ativo, data_cadastro
        FROM clientes
        WHERE id = ?
        """
        result = self.fetchone(query, (cliente_id,))
        if result:
            return dict(result)
        return None

    def get_by_name(self, nome: str):
        """Retorna um cliente por nome (busca exata)"""
        query = """
        SELECT id, nome, telefone, email, endereco, ativo, data_cadastro
        FROM clientes
        WHERE nome = ?
        """
        result = self.fetchone(query, (nome,))
        if result:
            return dict(result)
        return None

    def search_by_name(self, nome: str):
        """Busca clientes por nome (parcial)"""
        query = """
        SELECT id, nome, telefone, email, endereco, ativo, data_cadastro
        FROM clientes
        WHERE nome LIKE ? AND ativo = 1
        ORDER BY nome
        """
        results = self.fetchall(query, (f"%{nome}%",))
        return [dict(row) for row in results] if results else []

    def list_all(self):
        """Lista todos os clientes ativos"""
        query = """
        SELECT id, nome, telefone, email, endereco, ativo, data_cadastro
        FROM clientes
        WHERE ativo = 1
        ORDER BY nome
        """
        results = self.fetchall(query)
        return [dict(row) for row in results] if results else []

    def update(self, cliente_id: int, nome: str, telefone: str = "", email: str = "", endereco: str = ""):
        """Atualiza dados de um cliente"""
        query = """
        UPDATE clientes
        SET nome = ?, telefone = ?, email = ?, endereco = ?
        WHERE id = ?
        """
        self.execute(query, (nome, telefone, email, endereco, cliente_id))

    def delete(self, cliente_id: int):
        """Desativa um cliente (soft delete)"""
        query = """
        UPDATE clientes
        SET ativo = 0
        WHERE id = ?
        """
        self.execute(query, (cliente_id,))

    def get_saldo_cliente(self, cliente_id: int):
        """Retorna o saldo total pendente de um cliente (todos os fiados não quitados)"""
        query = """
        SELECT COALESCE(SUM(valor_pendente), 0) as saldo_pendente,
               COUNT(*) as total_fiados
        FROM fiados
        WHERE cliente_id = ? AND valor_pendente > 0
        """
        result = self.fetchone(query, (cliente_id,))
        if result:
            return dict(result)
        return {"saldo_pendente": 0, "total_fiados": 0}
