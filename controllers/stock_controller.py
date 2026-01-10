from services.stock_service import StockService

class StockController:

    def __init__(self):
        self.service = StockService()

    def entrada(self, produto_id, quantidade, valor_unitario, observacao=""):
        try:
            self.service.entrada_produto(
                produto_id,
                quantidade,
                valor_unitario,
                observacao
            )
            return {"success": True}
        except ValueError as e:
            return {"success": False, "error": str(e)}
        
    def saida(self, produto_id, quantidade, observacao=""):
        try:
            self.service.saida_produto(
                produto_id,
                quantidade,
                observacao
            )
            return {"success": True}
        except ValueError as e:
            return {"success": False, "error": str(e)}
