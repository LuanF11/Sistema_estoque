from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QLabel, QMessageBox
)
from PySide6.QtGui import QColor

from controllers.product_controller import ProductController

from ui.dialogs.product_form import ProductForm


class ProductWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.controller = ProductController()

        self._build_ui()
        self.load_products()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Barra superior
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar produto por nome ou tag")

        btn_search = QPushButton("Buscar")
        btn_search.clicked.connect(self.search_products)

        btn_new = QPushButton("Novo Produto")
        btn_delete = QPushButton("Deletar")
        btn_delete.clicked.connect(self.delete_product)

        top_bar.addWidget(QLabel("Produtos"))
        top_bar.addStretch()
        top_bar.addWidget(self.search_input)
        top_bar.addWidget(btn_search)
        top_bar.addWidget(btn_new)
        top_bar.addWidget(btn_delete)

        # Tabela
        self.table = QTableWidget()
        # self.table.setColumnCount(6)
        self.table.setColumnCount(8)
        # self.table.setHorizontalHeaderLabels([
        #     "ID", "Nome", "Quantidade", "Valor Compra",
        #     "Valor Venda", "Validade"
        # ])
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "Quantidade", "Estoque Mín.", "Valor Compra",
            "Valor Venda", "Validade", "Tags"
        ])

        layout.addLayout(top_bar)
        layout.addWidget(self.table)

        btn_new.clicked.connect(self.new_product)
        self.table.cellDoubleClicked.connect(self.edit_product)
    
    def new_product(self):
        dialog = ProductForm(self)
        if dialog.exec():
            self.load_products()

    def edit_product(self, row, column):
        produto_id = int(self.table.item(row, 0).text())
        product = self.controller.service.product_repo.get_by_id(produto_id)

        dialog = ProductForm(self, product=product)
        if dialog.exec():
            self.load_products()

    def delete_product(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Aviso", "Selecione um produto para deletar")
            return
        
        row = selected_rows[0].row()
        produto_id = int(self.table.item(row, 0).text())
        product_name = self.table.item(row, 1).text()
        
        reply = QMessageBox.question(
            self,
            "Confirmar Deleção",
            f"Tem certeza que deseja deletar '{product_name}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            self.controller.service.product_repo.delete(produto_id)
            self.load_products()
            QMessageBox.information(self, "Sucesso", "Produto deletado com sucesso")

    def load_products(self):
        products = self.controller.list_products()
        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(product["nome"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(product["quantidade"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(product.get("estoque_minimo", 5))))
            self.table.setItem(row, 4, QTableWidgetItem(f"{product['valor_compra']:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{product['valor_venda']:.2f}"))
            from utils.dates import format_date
            self.table.setItem(
                row, 6,
                QTableWidgetItem(format_date(product["data_validade"]))
            )
            self.table.setItem(row, 7, QTableWidgetItem(product.get("tags", "")))

            # Verificar status de aviso (estoque baixo ou validade)
            alertas = self.controller.service.get_product_alert_status(product, 7)
            # Prioridade: Vencido > Perto do vencimento > Estoque baixo
            if "Vencido" in alertas:
                color = QColor(64, 64, 64, 100)  # Cinza escuro com transparência
            elif "Perto do vencimento" in alertas:
                color = QColor(255, 0, 0, 100)  # Vermelho com transparência
            elif "Estoque baixo" in alertas:
                color = QColor(255, 255, 0, 100)  # Amarelo com transparência
            else:
                color = QColor(255, 255, 255, 0)  # Branco transparente (padrão)

            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(color)

    def search_products(self):
        nome = self.search_input.text()
        # products = self.controller.search_by_name(nome)
        products = self.controller.search_by_name_or_tag(nome)

        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(product["nome"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(product["quantidade"])))
            self.table.setItem(row, 3, QTableWidgetItem(str(product.get("estoque_minimo", 5))))
            self.table.setItem(row, 4, QTableWidgetItem(f"{product['valor_compra']:.2f}"))
            self.table.setItem(row, 5, QTableWidgetItem(f"{product['valor_venda']:.2f}"))
            from utils.dates import format_date
            self.table.setItem(
                row, 6,
                QTableWidgetItem(format_date(product["data_validade"]))
            )
            self.table.setItem(row, 7, QTableWidgetItem(product.get("tags", "")))

            # Verificar status de aviso (estoque baixo ou validade)
            alertas = self.controller.service.get_product_alert_status(product, 7)
            # Prioridade: Vencido > Perto do vencimento > Estoque baixo
            if "Vencido" in alertas:
                color = QColor(64, 64, 64, 100)  # Cinza escuro com transparência
            elif "Perto do vencimento" in alertas:
                color = QColor(255, 0, 0, 100)  # Vermelho com transparência
            elif "Estoque baixo" in alertas:
                color = QColor(255, 255, 0, 100)  # Amarelo com transparência
            else:
                color = QColor(255, 255, 255, 0)  # Branco transparente (padrão)

            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(color)
