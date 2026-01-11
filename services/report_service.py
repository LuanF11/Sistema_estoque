class ReportService:

    def __init__(self, repository):
        self.repository = repository

    def get_report(self, start_date, end_date):
        data = self.repository.get_sales_summary(start_date, end_date)

        faturamento_total = sum(row[3] for row in data) if data else 0
        lucro_total = sum(row[4] for row in data) if data else 0

        top_product = None
        if data:
            top_product = {
                "id": data[0][0],
                "nome": data[0][1],
                "quantidade": data[0][2]
            }

        return {
            "success": True,
            "data": data,
            "top_product": top_product,
            "totals": {
                "faturamento": faturamento_total,
                "lucro": lucro_total
            }
        }
