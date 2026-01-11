from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QHBoxLayout,
    QLineEdit, QSpinBox, QDoubleSpinBox, QDateEdit,
    QPushButton, QMessageBox, QCheckBox, QWidget, QLabel
)
from PySide6.QtWidgets import QSpinBox
from PySide6.QtCore import QDate
from controllers.product_controller import ProductController
from controllers.tag_controller import TagController


class ProductForm(QDialog):

    def __init__(self, parent=None, product=None):
        super().__init__(parent)

        self.controller = ProductController()
        self.tag_controller = TagController()
        self.product = product  # None = novo | dict = edição

        self.setWindowTitle("Produto")
        self.setMinimumWidth(420)

        self._build_ui()
        self._load_tags()

        if self.product:
            self._load_product()

    def _build_ui(self):

        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.nome_input = QLineEdit()

        self.quantidade_input = QSpinBox()
        self.quantidade_input.setMaximum(10**9)

        self.valor_compra_input = QDoubleSpinBox()
        self.valor_compra_input.setMaximum(10**9)
        self.valor_compra_input.setDecimals(2)

        self.valor_venda_input = QDoubleSpinBox()
        self.valor_venda_input.setMaximum(10**9)
        self.valor_venda_input.setDecimals(2)

        self.validade_input = QDateEdit()
        self.validade_input.setCalendarPopup(True)
        self.validade_input.setSpecialValueText("Sem validade")
        self.validade_input.setDate(QDate.currentDate())
        self.validade_input.setMinimumDate(QDate(1900, 1, 1))

        self.ativo_check = QCheckBox("Produto ativo")
        self.ativo_check.setChecked(True)

        form.addRow("Nome:", self.nome_input)
        form.addRow("Quantidade:", self.quantidade_input)
        form.addRow("Valor de compra:", self.valor_compra_input)
        form.addRow("Valor de venda:", self.valor_venda_input)
        form.addRow("Data de validade:", self.validade_input)
        form.addRow("", self.ativo_check)

        layout.addLayout(form)

        # Tags
        layout.addWidget(QLabel("Tags"))
        self.tags_container = QWidget()
        self.tags_layout = QVBoxLayout(self.tags_container)
        layout.addWidget(self.tags_container)

        # Botões
        buttons = QHBoxLayout()
        btn_save = QPushButton("Salvar")
        btn_cancel = QPushButton("Cancelar")

        btn_save.clicked.connect(self._save)
        btn_cancel.clicked.connect(self.reject)

        buttons.addStretch()
        buttons.addWidget(btn_save)
        buttons.addWidget(btn_cancel)

        layout.addLayout(buttons)


    def _load_tags(self):
        self.tag_checks = []
        tags = self.tag_controller.list_tags()

        for tag in tags:
            cb = QCheckBox(tag["nome"])
            cb.tag_id = tag["id"]
            self.tags_layout.addWidget(cb)
            self.tag_checks.append(cb)

    def _load_product(self):
        self.nome_input.setText(self.product["nome"])
        self.quantidade_input.setValue(self.product["quantidade"])
        self.valor_compra_input.setValue(self.product["valor_compra"])
        self.valor_venda_input.setValue(self.product["valor_venda"])
        self.ativo_check.setChecked(bool(self.product["ativo"]))

        if self.product["data_validade"]:
            y, m, d = map(int, self.product["data_validade"].split("-"))
            self.validade_input.setDate(QDate(y, m, d))

    def _save(self):
        nome = self.nome_input.text().strip()
        quantidade = self.quantidade_input.value()
        valor_compra = self.valor_compra_input.value()
        valor_venda = self.valor_venda_input.value()
        ativo = self.ativo_check.isChecked()

        data_validade = None
        if self.validade_input.date():
            data_validade = self.validade_input.date().toString("yyyy-MM-dd")

        tag_ids = [cb.tag_id for cb in self.tag_checks if cb.isChecked()]

        if self.product:
            result = self.controller.update_product(
                self.product["id"],
                nome,
                quantidade,
                valor_compra,
                valor_venda,
                data_validade,
                ativo,
                
                tag_ids
            )
        else:
            result = self.controller.create_product(
                nome,
                quantidade,
                valor_compra,
                valor_venda,
                data_validade,
                
                tag_ids
            )

        if result.get("success"):
            self.accept()
        else:
            QMessageBox.warning(self, "Erro", result.get("error", "Erro desconhecido"))
