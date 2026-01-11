from services.stock_service import StockService


class StockController:

    def __init__(self):
        self.service = StockService()

    def register_movement(
        self,
        produto_id: int,
        tipo: str,
        quantidade: int,
        observacao: str = ""
    ):
        try:
            if tipo == "ENTRADA":
                self.service.entrada_produto(
                    produto_id=produto_id,
                    quantidade=quantidade,
                    observacao=observacao
                )

            elif tipo == "SAIDA":
                self.service.saida_produto(
                    produto_id=produto_id,
                    quantidade=quantidade,
                    observacao=observacao
                )

            else:
                return {
                    "success": False,
                    "error": "Tipo de movimentação inválido"
                }

            return {"success": True}

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
