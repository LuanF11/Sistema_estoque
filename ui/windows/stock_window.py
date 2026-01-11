from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox,
    QTextEdit, QPushButton,
    QMessageBox
)
from controllers.stock_controller import StockController
from controllers.product_controller import ProductController


class StockWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.stock_controller = StockController()
        self.product_controller = ProductController()
        self._build_ui()
        self.load_products()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Movimentação de Estoque"))

        # Produto
        self.product_combo = QComboBox()
        layout.addWidget(QLabel("Produto"))
        layout.addWidget(self.product_combo)

        # Tipo de movimentação
        self.type_combo = QComboBox()
        self.type_combo.addItems(["ENTRADA", "SAIDA"])
        layout.addWidget(QLabel("Tipo de Movimentação"))
        layout.addWidget(self.type_combo)

        # Quantidade
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(1_000_000)
        layout.addWidget(QLabel("Quantidade"))
        layout.addWidget(self.quantity_input)

        # Observação
        self.observation_input = QTextEdit()
        self.observation_input.setPlaceholderText("Observação (opcional)")
        layout.addWidget(QLabel("Observação"))
        layout.addWidget(self.observation_input)

        # Botão registrar
        btn_register = QPushButton("Registrar Movimentação")
        btn_register.clicked.connect(self.register_movement)
        layout.addWidget(btn_register)

    def load_products(self):
        """
        Carrega produtos no combo.
        """
        self.product_combo.clear()
        products = self.product_controller.list_products()

        for product in products:
            self.product_combo.addItem(
                f"{product['nome']} (Estoque: {product['quantidade']})",
                product["id"]
            )

    def register_movement(self):
        produto_id = self.product_combo.currentData()
        tipo = self.type_combo.currentText()
        quantidade = self.quantity_input.value()
        observacao = self.observation_input.toPlainText().strip()

        result = self.stock_controller.register_movement(
            produto_id=produto_id,
            tipo=tipo,
            quantidade=quantidade,
            observacao=observacao
        )

        if result.get("success"):
            QMessageBox.information(self, "Sucesso", "Movimentação registrada com sucesso")
            self.quantity_input.setValue(1)
            self.observation_input.clear()
            self.load_products()  # Atualiza estoque visível
        else:
            QMessageBox.warning(self, "Erro", result.get("error", "Erro ao registrar movimentação"))
