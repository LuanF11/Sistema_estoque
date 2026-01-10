from services.report_service import ReportService

class ReportController:

    def __init__(self):
        self.service = ReportService()

    def sales_report(self, data_inicio, data_fim):
        return self.service.sales_report(data_inicio, data_fim)