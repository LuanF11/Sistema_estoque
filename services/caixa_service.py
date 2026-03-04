from datetime import date
from repositories.caixa_repository import CaixaRepository
from repositories.caixa_movimentacao_repository import CaixaMovimentacaoRepository
from models.caixa import Caixa


class CaixaService:

    def __init__(self):
        self.repository = CaixaRepository()
        self.mov_repository = CaixaMovimentacaoRepository()

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
        """Retorna dados do caixa de hoje e informa saldo esperado (considerando vendas e movimentos avulsos)."""
        caixa = self.repository.find_today_caixa()
        if not caixa:
            return None

        # Data de hoje
        hoje = date.today().isoformat()

        # Soma de vendas (movimentacoes tipo SAIDA ligadas a produtos)
        query_sales = """
            SELECT IFNULL(SUM(m.quantidade * p.valor_venda), 0)
            FROM movimentacoes m
            JOIN produtos p ON p.id = m.produto_id
            WHERE m.tipo = 'SAIDA' AND DATE(m.data_movimentacao) = DATE(?)
        """
        sales_total = self.repository.fetchone(query_sales, (hoje,))[0]

        # Movimentações avulsas de caixa (entradas/saidas)
        entradas_avulsas = self.mov_repository.sum_by_date(hoje, "ENTRADA") or 0
        saidas_avulsas = self.mov_repository.sum_by_date(hoje, "SAIDA") or 0

        # Cálculo do saldo esperado: abertura + vendas (faturamento) + entradas avulsas - saídas avulsas
        saldo_esperado = caixa["valor_abertura"] + sales_total + entradas_avulsas - saidas_avulsas

        # Retorna caixa enriquecido com informações financeiras
        caixa["faturamento_vendas"] = sales_total
        caixa["entradas_avulsas"] = entradas_avulsas
        caixa["saidas_avulsas"] = saidas_avulsas
        caixa["saldo_esperado"] = saldo_esperado

        return caixa

    def registrar_movimentacao_caixa(self, caixa_id: int | None, tipo: str, valor: float, descricao: str = "", categoria: str | None = None) -> dict:
        """Registra uma movimentação avulsa de caixa."""
        try:
            if tipo not in ("ENTRADA", "SAIDA"):
                return {"success": False, "error": "Tipo inválido"}

            if valor <= 0:
                return {"success": False, "error": "Valor deve ser maior que zero"}

            self.mov_repository.register(caixa_id, tipo, valor, descricao, categoria)
            return {"success": True, "message": "Movimentação registrada com sucesso"}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_caixa_aberto(self) -> dict | None:
        """Retorna caixa aberto (se houver)."""
        return self.repository.find_open_caixa()
