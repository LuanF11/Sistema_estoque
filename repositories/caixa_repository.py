from datetime import datetime, date
from repositories.base_repository import BaseRepository
from models.caixa import Caixa


class CaixaRepository(BaseRepository):

    def create(self, caixa: Caixa) -> int:
        """Cria novo registro de caixa e retorna o ID."""
        query = """
            INSERT INTO caixa (data, valor_abertura, status, data_abertura)
            VALUES (?, ?, ?, ?)
        """
        params = (caixa.data, caixa.valor_abertura, caixa.status, datetime.now())
        self.execute(query, params)
        
        # Retorna o ID do caixa criado
        result = self.fetchone("SELECT last_insert_rowid() as id")
        return result[0] if result else None

    def find_by_date(self, data: str) -> dict | None:
        """Busca caixa por data."""
        query = "SELECT * FROM caixa WHERE data = ?"
        result = self.fetchone(query, (data,))
        return self._map_to_dict(result) if result else None

    def find_today_caixa(self) -> dict | None:
        """Busca caixa de hoje."""
        today = date.today().isoformat()
        return self.find_by_date(today)

    def find_open_caixa(self) -> dict | None:
        """Busca caixa aberto (ABERTO)."""
        query = "SELECT * FROM caixa WHERE status = 'ABERTO' LIMIT 1"
        result = self.fetchone(query)
        return self._map_to_dict(result) if result else None

    def update_close(self, caixa_id: int, valor_fechamento: float) -> None:
        """Fecha o caixa com valor de fechamento."""
        query = """
            UPDATE caixa 
            SET valor_fechamento = ?, status = 'FECHADO', data_fechamento = ?
            WHERE id = ?
        """
        params = (valor_fechamento, datetime.now(), caixa_id)
        self.execute(query, params)

    def find_by_id(self, caixa_id: int) -> dict | None:
        """Busca caixa por ID."""
        query = "SELECT * FROM caixa WHERE id = ?"
        result = self.fetchone(query, (caixa_id,))
        return self._map_to_dict(result) if result else None

    def get_all(self) -> list[dict]:
        """Retorna todos os caixas."""
        query = "SELECT * FROM caixa ORDER BY data DESC"
        results = self.fetchall(query)
        return [self._map_to_dict(r) for r in results]

    def _map_to_dict(self, row: tuple) -> dict | None:
        """Converte linha do banco para dicionário."""
        if not row:
            return None
        
        return {
            "id": row[0],
            "data": row[1],
            "valor_abertura": row[2],
            "valor_fechamento": row[3],
            "status": row[4],
            "data_abertura": row[5],
            "data_fechamento": row[6]
        }
