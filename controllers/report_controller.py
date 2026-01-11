from services.report_service import ReportService
from repositories.report_repository import ReportRepository

class ReportController:

    def __init__(self):
        self.service = ReportService(ReportRepository())

    def generate_report(self, data_inicio, data_fim):
        return self.service.get_report(data_inicio, data_fim)