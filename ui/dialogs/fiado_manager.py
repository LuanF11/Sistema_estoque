from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QTableWidget,
    QTableWidgetItem, QPushButton, QMessageBox
)
from controllers.stock_controller import StockController
from controllers.product_controller import ProductController
from utils.dates import format_date


class FiadoManagerDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Fiados")
        self.resize(850, 400)

        self.controller = StockController()
        self.product_controller = ProductController()

        self._build_ui()
        self._load_fiados()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        label = QLabel("Fiados em aberto")
        layout.addWidget(label)

        self.table = QTableWidget(0, 7)
        self.table.setHorizontalHeaderLabels(["ID", "Cliente", "Produto", "Qtd", "Valor", "Observação", "Data"])                
        layout.addWidget(self.table)

        btn_layout = QHBoxLayout()
        self.btn_pay = QPushButton("Marcar como Pago")
        self.btn_pay.clicked.connect(self._pay_selected)
        self.btn_delete = QPushButton("Excluir Fiado")
        self.btn_delete.clicked.connect(self._delete_selected)
        self.btn_close = QPushButton("Fechar")
        self.btn_close.clicked.connect(self.close)

        btn_layout.addWidget(self.btn_pay)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_close)
        layout.addLayout(btn_layout)

    def _load_fiados(self):
        self.table.setRowCount(0)
        resp = self.controller.list_open_fiados()
        if not resp.get("success"):
            QMessageBox.warning(self, "Erro", resp.get("error", "Erro ao carregar fiados"))
            return

        fiados = resp.get("fiados", [])

        # fiado rows: (id, produto_id, quantidade, valor_unitario, valor_total, cliente, observacao, data_fiado)
        products = {p['id']: p for p in self.product_controller.list_products()}

        for f in fiados:
            row = self.table.rowCount()
            self.table.insertRow(row)
            produto = products.get(f.get('produto_id'), {"nome": "-"})

            self.table.setItem(row, 0, QTableWidgetItem(str(f['id'])))
            self.table.setItem(row, 1, QTableWidgetItem(str(f['cliente_nome'])))
            self.table.setItem(row, 2, QTableWidgetItem(str(produto.get('nome', '-'))))
            self.table.setItem(row, 3, QTableWidgetItem(str(f['quantidade'])))
            self.table.setItem(row, 4, QTableWidgetItem(f"R$ {f['valor_total']:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(str(f.get('observacao') or "-")))
            self.table.setItem(row, 6, QTableWidgetItem(format_date(str(f['data_fiado']))))

    def _pay_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Info", "Selecione um fiado para marcar como pago.")
            return

        fiado_id = int(self.table.item(row, 0).text())

        confirm = QMessageBox.question(self, "Confirmar", "Marcar fiado como pago? Esta ação irá contabilizar a venda no sistema.")
        if confirm != QMessageBox.StandardButton.Yes:
            return

        resp = self.controller.pay_fiado(fiado_id)
        if resp.get("success"):
            QMessageBox.information(self, "Sucesso", "Fiado marcado como pago e contabilizado.")
            self._load_fiados()
        else:
            QMessageBox.warning(self, "Erro", resp.get("error", "Erro ao pagar fiado"))

    def _delete_selected(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Info", "Selecione um fiado para excluir.")
            return

        fiado_id = int(self.table.item(row, 0).text())
        confirm = QMessageBox.question(
            self,
            "Confirmar",
            "Deseja realmente excluir o fiado selecionado? O estoque será reposto.",
            QMessageBox.Yes | QMessageBox.No
        )
        if confirm != QMessageBox.StandardButton.Yes:
            return

        resp = self.controller.delete_fiado(fiado_id)
        if resp.get("success"):
            QMessageBox.information(self, "Sucesso", "Fiado excluído e estoque ajustado.")
            self._load_fiados()
        else:
            QMessageBox.warning(self, "Erro", resp.get("error", "Erro ao excluir fiado"))
