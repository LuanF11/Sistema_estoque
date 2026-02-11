from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox,
    QSpinBox, QTextEdit, QPushButton, QMessageBox
)
from controllers.stock_controller import StockController
from controllers.product_controller import ProductController


class PrejuizoDialog(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Registrar Prejuízo")
        self.resize(450, 300)

        self.controller = StockController()
        self.product_controller = ProductController()

        self._build_ui()
        self._load_products()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Produto:"))
        self.product_combo = QComboBox()
        layout.addWidget(self.product_combo)

        layout.addWidget(QLabel("Quantidade:"))
        self.quantity_spin = QSpinBox()
        self.quantity_spin.setMinimum(1)
        self.quantity_spin.setMaximum(1_000_000)
        layout.addWidget(self.quantity_spin)

        layout.addWidget(QLabel("Motivo:"))
        self.motivo_combo = QComboBox()
        self.motivo_combo.addItems(["Quebrado", "Vazamento", "Defeito", "Outro"])
        layout.addWidget(self.motivo_combo)

        layout.addWidget(QLabel("Observação (opcional):"))
        self.obs = QTextEdit()
        self.obs.setMaximumHeight(80)
        layout.addWidget(self.obs)

        btn_layout = QHBoxLayout()
        self.btn_ok = QPushButton("Registrar")
        self.btn_ok.clicked.connect(self._on_register)
        self.btn_cancel = QPushButton("Cancelar")
        self.btn_cancel.clicked.connect(self.reject)
        btn_layout.addWidget(self.btn_ok)
        btn_layout.addWidget(self.btn_cancel)

        layout.addLayout(btn_layout)

    def _load_products(self):
        products = self.product_controller.list_products()
        self.product_combo.clear()
        for p in products:
            self.product_combo.addItem(f"{p['nome']}", p['id'])

    def _on_register(self):
        produto_id = self.product_combo.currentData()
        quantidade = self.quantity_spin.value()
        motivo = self.motivo_combo.currentText()
        observacao = self.obs.toPlainText().strip()

        if not produto_id:
            QMessageBox.warning(self, "Aviso", "Selecione um produto")
            return

        resp = self.controller.register_prejuizo(produto_id, quantidade, motivo, observacao)
        if resp.get('success'):
            QMessageBox.information(self, "Sucesso", "Prejuízo registrado com sucesso")
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", resp.get('error', 'Erro ao registrar prejuízo'))
