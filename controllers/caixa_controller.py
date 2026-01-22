from services.caixa_service import CaixaService


class CaixaController:

    def __init__(self):
        self.service = CaixaService()

    def abrir_caixa(self, valor_abertura: float) -> dict:
        """Abre um novo caixa."""
        return self.service.abrir_caixa(valor_abertura)

    def fechar_caixa(self, caixa_id: int, valor_fechamento: float) -> dict:
        """Fecha o caixa."""
        return self.service.fechar_caixa(caixa_id, valor_fechamento)

    def get_caixa_hoje(self) -> dict | None:
        """Retorna caixa de hoje."""
        return self.service.get_caixa_hoje()

    def get_caixa_aberto(self) -> dict | None:
        """Retorna caixa aberto."""
        return self.service.get_caixa_aberto()
