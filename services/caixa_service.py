from datetime import date
from repositories.caixa_repository import CaixaRepository
from models.caixa import Caixa


class CaixaService:

    def __init__(self):
        self.repository = CaixaRepository()

    def abrir_caixa(self, valor_abertura: float) -> dict:
        """Abre um novo caixa para o dia."""
        try:
            # Verifica se já existe caixa aberto
            caixa_aberto = self.repository.find_open_caixa()
            if caixa_aberto:
                return {
                    "success": False,
                    "error": "Já existe um caixa aberto"
                }

            # Verifica se já existe caixa para hoje
            today = date.today().isoformat()
            caixa_hoje = self.repository.find_by_date(today)
            if caixa_hoje:
                return {
                    "success": False,
                    "error": "Caixa já foi aberto hoje"
                }

            # Valida valor de abertura
            if valor_abertura < 0:
                return {
                    "success": False,
                    "error": "Valor de abertura não pode ser negativo"
                }

            # Cria novo caixa
            caixa = Caixa(
                id=None,
                data=today,
                valor_abertura=valor_abertura,
                status="ABERTO"
            )
            
            caixa_id = self.repository.create(caixa)
            
            return {
                "success": True,
                "caixa_id": caixa_id,
                "message": "Caixa aberto com sucesso"
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def fechar_caixa(self, caixa_id: int, valor_fechamento: float) -> dict:
        """Fecha o caixa do dia."""
        try:
            # Busca caixa
            caixa = self.repository.find_by_id(caixa_id)
            if not caixa:
                return {
                    "success": False,
                    "error": "Caixa não encontrado"
                }

            # Verifica se já está fechado
            if caixa["status"] == "FECHADO":
                return {
                    "success": False,
                    "error": "Este caixa já foi fechado"
                }

            # Valida valor de fechamento
            if valor_fechamento < 0:
                return {
                    "success": False,
                    "error": "Valor de fechamento não pode ser negativo"
                }

            # Fecha o caixa
            self.repository.update_close(caixa_id, valor_fechamento)

            # Calcula diferença
            diferenca = valor_fechamento - caixa["valor_abertura"]

            return {
                "success": True,
                "message": "Caixa fechado com sucesso",
                "valor_abertura": caixa["valor_abertura"],
                "valor_fechamento": valor_fechamento,
                "diferenca": diferenca
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    def get_caixa_hoje(self) -> dict | None:
        """Retorna dados do caixa de hoje."""
        return self.repository.find_today_caixa()

    def get_caixa_aberto(self) -> dict | None:
        """Retorna caixa aberto (se houver)."""
        return self.repository.find_open_caixa()
