from repositories.stock_repository import StockRepository
from repositories.product_repository import ProductRepository

class ReportService:
    '''
    Classe responsável por gerar relatórios relacionados ao estoque e produtos.
    '''

    def __init__(self):
        self.stock_repo = StockRepository()
        self.product_repo = ProductRepository()

    def sales_report(self, data_inicio: str, data_fim: str):
        movimentacoes = self.stock_repo.list_by_period(data_inicio, data_fim)

        total_vendas = 0
        lucro_total = 0
        ranking = {}

        for mov in movimentacoes:
            if mov["tipo"] == "SAIDA":
                produto = self.product_repo.get_by_id(mov["produto_id"])
                total_vendas += mov["quantidade"] * mov["valor_unitario"]

                lucro = (mov["valor_unitario"] - produto["valor_compra"]) * mov["quantidade"]
                lucro_total += lucro

                ranking[produto["nome"]] = ranking.get(produto["nome"], 0) + mov["quantidade"]

        produto_mais_vendido = max(ranking, key=ranking.get) if ranking else None

        return {
            "total_vendas": total_vendas,
            "lucro_total": lucro_total,
            "produto_mais_vendido": produto_mais_vendido,
            "ranking": ranking
        }