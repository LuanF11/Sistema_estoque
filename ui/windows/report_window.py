from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QTableWidget,
    QTableWidgetItem, QMessageBox, QDateEdit
)
from PySide6.QtCore import QDate
from controllers.report_controller import ReportController


class ReportWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.controller = ReportController()
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Relatórios de Vendas"))

        # Filtros de data
        filters = QHBoxLayout()
        self.start_date = QDateEdit(QDate.currentDate().addMonths(-1))
        self.end_date = QDateEdit(QDate.currentDate())
        self.start_date.setCalendarPopup(True)
        self.end_date.setCalendarPopup(True)

        btn_generate = QPushButton("Gerar Relatório")
        btn_generate.clicked.connect(self.generate_report)

        filters.addWidget(QLabel("Início"))
        filters.addWidget(self.start_date)
        filters.addWidget(QLabel("Fim"))
        filters.addWidget(self.end_date)
        filters.addWidget(btn_generate)

        layout.addLayout(filters)

        # Tabela
        self.table = QTableWidget(0, 5)
        self.table.setHorizontalHeaderLabels([
            "Produto", "Qtd Vendida", "Faturamento", "Lucro", "ID"
        ])
        self.table.setColumnHidden(4, True)

        layout.addWidget(self.table)

        # Resumo
        self.summary_label = QLabel()
        layout.addWidget(self.summary_label)

    def generate_report(self):
        start = self.start_date.date().toString("yyyy-MM-dd")
        end = self.end_date.date().toString("yyyy-MM-dd")

        result = self.controller.generate_report(start, end)

        if not result.get("success"):
            QMessageBox.warning(self, "Erro", "Erro ao gerar relatório")
            return

        self.table.setRowCount(0)

        for row_data in result["data"]:
            row = self.table.rowCount()
            self.table.insertRow(row)

            self.table.setItem(row, 0, QTableWidgetItem(row_data[1]))
            self.table.setItem(row, 1, QTableWidgetItem(str(row_data[2])))
            self.table.setItem(row, 2, QTableWidgetItem(f"R$ {row_data[3]:.2f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"R$ {row_data[4]:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(str(row_data[0])))

        totals = result["totals"]
        top = result["top_product"]

        text = (
            f"Faturamento Total: R$ {totals['faturamento']:.2f}\n"
            f"Lucro Total: R$ {totals['lucro']:.2f}"
        )

        if top:
            text += f"\nProduto Mais Vendido: {top['nome']} ({top['quantidade']} unidades)"

        self.summary_label.setText(text)
