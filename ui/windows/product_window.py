from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QLabel
)
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

        top_bar.addWidget(QLabel("Produtos"))
        top_bar.addStretch()
        top_bar.addWidget(self.search_input)
        top_bar.addWidget(btn_search)
        top_bar.addWidget(btn_new)

        # Tabela
        self.table = QTableWidget()
        # self.table.setColumnCount(6)
        self.table.setColumnCount(7)
        # self.table.setHorizontalHeaderLabels([
        #     "ID", "Nome", "Quantidade", "Valor Compra",
        #     "Valor Venda", "Validade"
        # ])
        self.table.setHorizontalHeaderLabels([
            "ID", "Nome", "Quantidade", "Valor Compra",
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

    def load_products(self):
        products = self.controller.list_products()
        self.table.setRowCount(len(products))

        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(product["nome"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(product["quantidade"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{product['valor_compra']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{product['valor_venda']:.2f}"))
            self.table.setItem(
                row, 5,
                QTableWidgetItem(product["data_validade"] or "-")
            )
            self.table.setItem(row, 6, QTableWidgetItem(product.get("tags", "")))

    def search_products(self):
        nome = self.search_input.text()
        # products = self.controller.search_by_name(nome)
        products = self.controller.search_by_name_or_tag(nome)

        self.table.setRowCount(len(products))
        for row, product in enumerate(products):
            self.table.setItem(row, 0, QTableWidgetItem(str(product["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(product["nome"]))
            self.table.setItem(row, 2, QTableWidgetItem(str(product["quantidade"])))
            self.table.setItem(row, 3, QTableWidgetItem(f"{product['valor_compra']:.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{product['valor_venda']:.2f}"))
            self.table.setItem(
                row, 5,
                QTableWidgetItem(product["data_validade"] or "-")
            )
            self.table.setItem(row, 6, QTableWidgetItem(product.get("tags", "")))
