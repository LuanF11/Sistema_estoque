from services.stock_service import StockService


class StockController:

    def __init__(self):
        self.service = StockService()

    def register_movement(
        self,
        produto_id: int,
        tipo: str,
        quantidade: int,
        observacao: str = "",
        fiado: bool = False,
        cliente: str | None = None
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
                    observacao=observacao,
                    fiado=fiado,
                    cliente=cliente
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

    def list_open_fiados(self):
        try:
            fiados = self.service.list_open_fiados()
            return {"success": True, "fiados": fiados}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def pay_fiado(self, fiado_id: int):
        try:
            self.service.pay_fiado(fiado_id)
            return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}
