from datetime import datetime, timedelta
from repositories.analytics_repository import AnalyticsRepository


class AnalyticsService:
    """Serviço de análises avançadas de dados"""

    def __init__(self):
        self.repository = AnalyticsRepository()

    def get_sales_chart_data(self, days=30):
        """Dados para gráfico de vendas"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        data = self.repository.get_sales_by_period(start_date, end_date)
        
        if not data:
            return [], []
        
        dates = [row[0] for row in data]
        faturamentos = [row[1] or 0 for row in data]
        
        return dates, faturamentos

    def get_profit_chart_data(self, days=30):
        """Dados para gráfico de lucro"""
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=days)
        
        data = self.repository.get_sales_by_period(start_date, end_date)
        
        if not data:
            return [], []
        
        dates = [row[0] for row in data]
        lucros = [row[2] or 0 for row in data]
        
        return dates, lucros

    def get_top_products_data(self, limit=10):
        """Dados dos produtos mais vendidos"""
        data = self.repository.get_top_products(limit)
        return [
            {
                "id": row[0],
                "nome": row[1],
                "quantidade": row[2],
                "faturamento": row[3] or 0,
                "lucro": row[4] or 0
            }
            for row in data
        ]

    def get_category_performance(self):
        """Desempenho por categoria"""
        data = self.repository.get_products_by_category()
        return [
            {
                "categoria": row[0],
                "produtos": row[1],
                "vendidas": row[2] or 0,
                "faturamento": row[3] or 0,
                "lucro": row[4] or 0
            }
            for row in data
        ]

    def get_stock_metrics(self):
        """Métricas de estoque"""
        data = self.repository.get_stock_value()
        
        if not data:
            return {
                "valor_custo": 0,
                "valor_venda": 0,
                "total_produtos": 0,
                "total_itens": 0
            }
        
        return {
            "valor_custo": data[0] or 0,
            "valor_venda": data[1] or 0,
            "total_produtos": data[2] or 0,
            "total_itens": data[3] or 0
        }

    def get_low_stock_alert(self):
        """Produtos com estoque baixo"""
        data = self.repository.get_low_stock_products()
        return [
            {
                "id": row[0],
                "nome": row[1],
                "quantidade": row[2],
                "minimo": row[3],
                "valor": row[4]
            }
            for row in data
        ]

    def get_turnover_analysis(self, days=30):
        """Análise de rotatividade"""
        data = self.repository.get_product_turnover(days)
        return [
            {
                "id": row[0],
                "nome": row[1],
                "movimentacoes": row[2],
                "saidas": row[3] or 0,
                "entradas": row[4] or 0
            }
            for row in data
        ]

    def get_profit_margins(self):
        """Margens de lucro por produto"""
        data = self.repository.get_profit_margin_by_product()
        return [
            {
                "id": row[0],
                "nome": row[1],
                "custo": row[2],
                "venda": row[3],
                "margem": row[4],
                "vendidas": row[5] or 0,
                "lucro_total": row[6] or 0
            }
            for row in data
        ]

    def get_expiring_products(self, days=30):
        """Produtos próximos do vencimento"""
        data = self.repository.get_expiring_products(days)
        return [
            {
                "id": row[0],
                "nome": row[1],
                "validade": row[2],
                "quantidade": row[3],
                "valor": row[4],
                "dias": row[5] or 0
            }
            for row in data
        ]

    def get_inactive_products(self, days=60):
        """Produtos encalhados sem movimentação"""
        data = self.repository.get_inactive_products(days)
        return [
            {
                "id": row[0],
                "nome": row[1],
                "quantidade": row[2],
                "data_cadastro": row[3],
                "valor": row[4],
                "dias_parado": row[5] or 999
            }
            for row in data
        ]

    def get_monthly_summary(self, months=12):
        """Resumo mensal"""
        data = self.repository.get_monthly_summary(months)
        return [
            {
                "mes": row[0],
                "qtd_vendida": row[1] or 0,
                "faturamento": row[2] or 0,
                "lucro": row[3] or 0
            }
            for row in data
        ]

    def get_fiados_summary(self):
        data = self.repository.get_fiados_summary()
        if not data:
            return {
                "count_open": 0,
                "total_open": 0,
                "count_paid": 0,
                "total_paid": 0
            }

        return {
            "count_open": data[0] or 0,
            "total_open": data[1] or 0,
            "count_paid": data[2] or 0,
            "total_paid": data[3] or 0
        }

    def get_prejuizos_summary(self):
        data = self.repository.get_prejuizos_summary()
        if not data:
            return {"count_total": 0, "total_valor": 0}
        return {"count_total": data[0] or 0, "total_valor": data[1] or 0}

    def get_prejuizos_by_motivo(self, limit=10):
        data = self.repository.get_prejuizos_by_motivo(limit)
        return [
            {"motivo": row[0], "count": row[1] or 0, "total": row[2] or 0}
            for row in data
        ]

    def get_cash_flow(self, start_date, end_date):
        """Fluxo de caixa"""
        data = self.repository.get_cash_flow_summary(start_date, end_date)
        return [
            {
                "data": row[0],
                "abertura": row[1],
                "fechamento": row[2],
                "vendas": row[3] or 0
            }
            for row in data
        ]

    def get_total_statistics(self):
        """Estatísticas gerais"""
        data = self.repository.get_total_statistics()
        
        if not data:
            return {
                "total_produtos": 0,
                "total_itens": 0,
                "total_vendas": 0,
                "dias_com_vendas": 0
            }
        
        return {
            "total_produtos": data[0] or 0,
            "total_itens": data[1] or 0,
            "total_vendas": data[2] or 0,
            "dias_com_vendas": data[3] or 0
        }

    def get_dashboard_data(self):
        """Agregação de todos os dados do dashboard"""
        return {
            "estatisticas": self.get_total_statistics(),
            "estoque": self.get_stock_metrics(),
            "produtos_top": self.get_top_products_data(5),
            "categorias": self.get_category_performance(),
            "alertas_estoque": self.get_low_stock_alert(),
            "produtos_prox_vencer": self.get_expiring_products(30),
        }
