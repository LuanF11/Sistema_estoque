from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QComboBox, QSpinBox, QDoubleSpinBox,
    QTextEdit, QPushButton,
    QMessageBox, QGroupBox
)
from PySide6.QtWidgets import QCheckBox, QLineEdit
from PySide6.QtCore import Qt
from controllers.stock_controller import StockController
from controllers.product_controller import ProductController
from controllers.caixa_controller import CaixaController


class StockWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.stock_controller = StockController()
        self.product_controller = ProductController()
        self.caixa_controller = CaixaController()
        self.current_stock = 0
        self._build_ui()
        self.load_products()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Título
        title = QLabel("Movimentação de Estoque")
        title_font = title.font()
        title_font.setPointSize(12)
        title_font.setBold(True)
        title.setFont(title_font)
        layout.addWidget(title)

        # Grupo de campos
        form_group = QGroupBox("Detalhes da Movimentação")
        form_layout = QVBoxLayout()
        form_layout.setSpacing(8)

        # Produto
        self.product_combo = QComboBox()
        self.product_combo.currentIndexChanged.connect(self._on_product_changed)
        form_layout.addWidget(QLabel("Produto:"))
        form_layout.addWidget(self.product_combo)

        # Label de estoque disponível
        self.stock_label = QLabel("Estoque disponível: -")
        self.stock_label.setStyleSheet("color: #666; font-style: italic;")
        form_layout.addWidget(self.stock_label)

        # Tipo de movimentação
        self.type_combo = QComboBox()
        self.type_combo.addItems(["ENTRADA", "SAIDA"])
        self.type_combo.currentTextChanged.connect(self._on_movement_type_changed)
        form_layout.addWidget(QLabel("Tipo de Movimentação:"))
        form_layout.addWidget(self.type_combo)

        # Quantidade
        self.quantity_input = QSpinBox()
        self.quantity_input.setMinimum(1)
        self.quantity_input.setMaximum(1_000_000)
        self.quantity_input.setValue(1)
        form_layout.addWidget(QLabel("Quantidade:"))
        form_layout.addWidget(self.quantity_input)

        # Observação
        self.observation_input = QTextEdit()
        self.observation_input.setPlaceholderText("Observação (opcional)")
        self.observation_input.setMaximumHeight(80)
        form_layout.addWidget(QLabel("Observação:"))
        form_layout.addWidget(self.observation_input)

        # Movimentação avulsa (não altera estoque) - registra direto no caixa
        self.avulso_checkbox = QCheckBox("Avulso (registrar no caixa)")
        self.avulso_checkbox.stateChanged.connect(self._on_avulso_changed)
        form_layout.addWidget(self.avulso_checkbox)

        self.spin_valor_avulso = QDoubleSpinBox()
        self.spin_valor_avulso.setMinimum(0)
        self.spin_valor_avulso.setMaximum(9999999)
        self.spin_valor_avulso.setDecimals(2)
        self.spin_valor_avulso.setEnabled(False)
        form_layout.addWidget(QLabel("Valor (R$) - apenas para avulso:"))
        form_layout.addWidget(self.spin_valor_avulso)

        # Fiado
        self.fiado_checkbox = QCheckBox("Fiado")
        self.fiado_checkbox.stateChanged.connect(self._on_fiado_changed)
        form_layout.addWidget(self.fiado_checkbox)

        self.cliente_input = QLineEdit()
        self.cliente_input.setPlaceholderText("Nome do cliente (apenas para fiado)")
        self.cliente_input.setEnabled(False)
        form_layout.addWidget(self.cliente_input)

        form_group.setLayout(form_layout)
        layout.addWidget(form_group)

        # Botões (layout horizontal)
        buttons_layout = QHBoxLayout()
        
        self.btn_register = QPushButton("Registrar Movimentação")
        self.btn_register.setMinimumHeight(40)
        self.btn_register.clicked.connect(self.register_movement)
        
        self.btn_clear = QPushButton("Limpar")
        self.btn_clear.setMinimumHeight(40)
        self.btn_clear.clicked.connect(self._clear_form)
        self.btn_clear.setMaximumWidth(120)
        
        self.btn_manage_fiados = QPushButton("Gerenciar Fiados")
        self.btn_manage_fiados.setMinimumHeight(40)
        self.btn_manage_fiados.clicked.connect(self._open_fiado_manager)
        self.btn_manage_fiados.setMaximumWidth(160)
        
        self.btn_register_prejuizo = QPushButton("Registrar Prejuízo")
        self.btn_register_prejuizo.setMinimumHeight(40)
        self.btn_register_prejuizo.clicked.connect(self._open_prejuizo_dialog)
        self.btn_register_prejuizo.setMaximumWidth(160)
        
        buttons_layout.addWidget(self.btn_register)
        buttons_layout.addWidget(self.btn_register_prejuizo)
        buttons_layout.addWidget(self.btn_manage_fiados)
        buttons_layout.addWidget(self.btn_clear)
        layout.addLayout(buttons_layout)

        layout.addStretch()
        self.setLayout(layout)

    def load_products(self):
        """
        Carrega produtos no combo.
        """
        self.product_combo.clear()
        products = self.product_controller.list_products()

        if not products:
            self.product_combo.addItem("Nenhum produto disponível", None)
            return

        for product in products:
            self.product_combo.addItem(
                f"{product['nome']}",
                product["id"]
            )
        
        # Atualiza estoque do primeiro produto
        if products:
            self.current_stock = products[0].get('quantidade', 0)
            self._update_stock_label()

    def _on_product_changed(self):
        """Atualiza o estoque quando o produto é alterado."""
        product_id = self.product_combo.currentData()
        if product_id:
            products = self.product_controller.list_products()
            for product in products:
                if product["id"] == product_id:
                    self.current_stock = product.get('quantidade', 0)
                    self._update_stock_label()
                    break

    def _on_movement_type_changed(self):
        """Restringe quantidade para saídas baseado no estoque disponível."""
        if self.type_combo.currentText() == "SAIDA":
            self.quantity_input.setMaximum(max(1, self.current_stock))
            if self.quantity_input.value() > self.current_stock:
                self.quantity_input.setValue(self.current_stock)
        else:
            self.quantity_input.setMaximum(1_000_000)

    def _update_stock_label(self):
        """Atualiza o label do estoque disponível."""
        self.stock_label.setText(f"Estoque disponível: {self.current_stock} unidades")

    def _clear_form(self):
        """Limpa o formulário."""
        self.quantity_input.setValue(1)
        self.observation_input.clear()
        self.fiado_checkbox.setChecked(False)
        self.cliente_input.clear()

    def register_movement(self):
        # Validações
        if not self.product_combo.currentData():
            QMessageBox.warning(self, "Aviso", "Selecione um produto")
            return

        produto_id = self.product_combo.currentData()
        tipo = self.type_combo.currentText()
        quantidade = self.quantity_input.value()
        observacao = self.observation_input.toPlainText().strip()
        fiado = bool(self.fiado_checkbox.isChecked())
        cliente = self.cliente_input.text().strip() if fiado else None

        avulso = bool(self.avulso_checkbox.isChecked())

        # Validação para saída
        if tipo == "SAIDA" and quantidade > self.current_stock:
            QMessageBox.warning(
                self, 
                "Estoque Insuficiente", 
                f"Quantidade em estoque: {self.current_stock} unidades\nQuantidade solicitada: {quantidade} unidades"
            )
            return

        # Desabilita botão durante processamento
        self.btn_register.setEnabled(False)
        self.btn_register.setText("Processando...")

        try:
            if avulso:
                # Registrar movimentação avulsa no caixa (valor informado pelo usuário)
                valor = float(self.spin_valor_avulso.value())
                # Para avulso, tipo deve ser ENTRADA ou SAIDA; se for SAIDA e foi marcado fiado, ignorar fiado
                result = self.caixa_controller.registrar_movimentacao_caixa(None, tipo, valor, observacao, None)
            else:
                result = self.stock_controller.register_movement(
                    produto_id=produto_id,
                    tipo=tipo,
                    quantidade=quantidade,
                    observacao=observacao,
                    fiado=fiado,
                    cliente=cliente
                )

            if result.get("success"):
                QMessageBox.information(
                    self, 
                    "Sucesso", 
                    "Movimentação registrada com sucesso"
                )
                self._clear_form()
                self.load_products()  # Atualiza estoque visível
            else:
                error_msg = result.get("error", "Erro ao registrar movimentação")
                QMessageBox.warning(self, "Erro", error_msg)
        finally:
            # Reabilita botão
            self.btn_register.setEnabled(True)
            self.btn_register.setText("Registrar Movimentação")

    def _on_fiado_changed(self):
        checked = self.fiado_checkbox.isChecked()
        if checked and self.type_combo.currentText() != "SAIDA":
            # Fiado faz sentido apenas para SAIDA
            QMessageBox.information(self, "Info", "Fiado só é aplicado em SAÍDA de produtos.")
            self.fiado_checkbox.setChecked(False)
            return

        self.cliente_input.setEnabled(checked)

    def _on_avulso_changed(self):
        """Handler para checkbox de movimentação avulsa.

        Habilita/desabilita o campo de valor avulso e desabilita o formulário de produto/quantidade
        para evitar alterações de estoque quando estiver registrando apenas uma movimentação no caixa.
        """
        checked = self.avulso_checkbox.isChecked()
        self.spin_valor_avulso.setEnabled(checked)
        # Quando for avulso, não alterar estoque: desabilita seleção de produto e quantidade
        self.product_combo.setEnabled(not checked)
        self.quantity_input.setEnabled(not checked)
        # Se ativou avulso, garante quantidade 1 como padrão
        if checked:
            self.quantity_input.setValue(1)

    def _open_fiado_manager(self):
        from ui.dialogs.fiado_manager import FiadoManagerDialog

        dlg = FiadoManagerDialog(self)
        dlg.exec()

    def _open_prejuizo_dialog(self):
        from ui.dialogs.prejuizo_dialog import PrejuizoDialog

        dlg = PrejuizoDialog(self)
        if dlg.exec():
            # atualiza lista de produtos/estoque visível
            self.load_products()
    def refresh(self):
        """Recarrega os dados quando a aba fica visível."""
        self.load_products()