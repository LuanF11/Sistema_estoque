from PySide6.QtWidgets import (
    QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QLineEdit,
    QPushButton, QTableWidget, QTableWidgetItem, QMessageBox, QDialog,
    QSpinBox, QDoubleSpinBox, QComboBox, QDateEdit, QTextEdit, QFormLayout
)
from PySide6.QtCore import Qt, QDate
from controllers.cliente_controller import ClienteController
from controllers.product_controller import ProductController
from utils.dates import format_date


class ClienteWindow(QMainWindow):
    """Janela principal para gerenciar clientes e fiados"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Gerenciar Clientes e Fiados")
        self.resize(1200, 700)

        self.controller = ClienteController()
        self.product_controller = ProductController()
        self.cliente_selecionado = None

        self._build_ui()

    def _build_ui(self):
        """Constrói a interface"""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QHBoxLayout(central_widget)

        # Painel esquerdo: Pesquisa e lista de clientes
        esquerdo = QVBoxLayout()

        # Seção de pesquisa
        label_pesquisa = QLabel("Pesquisar Cliente:")
        self.input_pesquisa = QLineEdit()
        self.input_pesquisa.setPlaceholderText("Digite o nome do cliente...")
        self.input_pesquisa.textChanged.connect(self._pesquisar_clientes)

        esquerdo.addWidget(label_pesquisa)
        esquerdo.addWidget(self.input_pesquisa)

        # Botão para criar novo cliente
        self.btn_novo_cliente = QPushButton("+ Novo Cliente")
        self.btn_novo_cliente.clicked.connect(self._abrir_dialog_novo_cliente)
        esquerdo.addWidget(self.btn_novo_cliente)

        # Tabela de clientes
        self.table_clientes = QTableWidget(0, 3)
        self.table_clientes.setHorizontalHeaderLabels(["ID", "Nome", "Saldo Pendente"])
        self.table_clientes.itemSelectionChanged.connect(self._cliente_selecionado)
        esquerdo.addWidget(self.table_clientes)

        # Painel direito: Detalhes do cliente e fiados
        direito = QVBoxLayout()

        # Informações do cliente selecionado
        label_cliente = QLabel("Detalhes do Cliente:")
        direito.addWidget(label_cliente)

        self.label_cliente_info = QLabel("Nenhum cliente selecionado")
        direito.addWidget(self.label_cliente_info)

        # Botões de ação para cliente
        btn_layout_cliente = QHBoxLayout()
        self.btn_editar_cliente = QPushButton("Editar Cliente")
        self.btn_editar_cliente.clicked.connect(self._abrir_dialog_editar_cliente)
        self.btn_editar_cliente.setEnabled(False)

        self.btn_deletar_cliente = QPushButton("Deletar Cliente")
        self.btn_deletar_cliente.clicked.connect(self._deletar_cliente)
        self.btn_deletar_cliente.setEnabled(False)

        btn_layout_cliente.addWidget(self.btn_editar_cliente)
        btn_layout_cliente.addWidget(self.btn_deletar_cliente)
        direito.addLayout(btn_layout_cliente)

        # Tabela de fiados do cliente
        label_fiados = QLabel("Fiados do Cliente:")
        direito.addWidget(label_fiados)

        self.table_fiados = QTableWidget(0, 6)
        self.table_fiados.setHorizontalHeaderLabels(
            ["ID", "Produto", "Quantidade", "Valor Total", "Valor Pendente", "Data"]
        )
        self.table_fiados.itemSelectionChanged.connect(self._fiado_selecionado)
        direito.addWidget(self.table_fiados)

        # Botões de ação para fiados
        btn_layout_fiados = QHBoxLayout()
        self.btn_novo_fiado = QPushButton("+ Novo Fiado")
        self.btn_novo_fiado.clicked.connect(self._abrir_dialog_novo_fiado)
        self.btn_novo_fiado.setEnabled(False)

        self.btn_adicionar_pagamento = QPushButton("Adicionar Pagamento")
        self.btn_adicionar_pagamento.clicked.connect(self._abrir_dialog_pagamento)
        self.btn_adicionar_pagamento.setEnabled(False)

        self.btn_deletar_fiado = QPushButton("Deletar Fiado")
        self.btn_deletar_fiado.clicked.connect(self._deletar_fiado)
        self.btn_deletar_fiado.setEnabled(False)

        self.btn_ver_pagamentos = QPushButton("Ver Pagamentos")
        self.btn_ver_pagamentos.clicked.connect(self._ver_pagamentos_fiado)
        self.btn_ver_pagamentos.setEnabled(False)

        btn_layout_fiados.addWidget(self.btn_novo_fiado)
        btn_layout_fiados.addWidget(self.btn_adicionar_pagamento)
        btn_layout_fiados.addWidget(self.btn_ver_pagamentos)
        btn_layout_fiados.addWidget(self.btn_deletar_fiado)
        direito.addLayout(btn_layout_fiados)

        # Adicionar os painéis ao layout principal
        layout.addLayout(esquerdo, 1)
        layout.addLayout(direito, 2)

        # Carregar dados iniciais
        self._listar_clientes()

    def _pesquisar_clientes(self):
        """Busca clientes por nome"""
        texto = self.input_pesquisa.text()
        if texto.strip():
            resp = self.controller.pesquisar_cliente(texto)
        else:
            resp = self.controller.listar_clientes()

        if resp.get("success"):
            self._preencher_tabela_clientes(resp.get("clientes", []))
        else:
            QMessageBox.warning(self, "Erro", resp.get("error", "Erro ao pesquisar clientes"))

    def _listar_clientes(self):
        """Lista todos os clientes"""
        resp = self.controller.listar_clientes()
        if resp.get("success"):
            self._preencher_tabela_clientes(resp.get("clientes", []))
        else:
            QMessageBox.warning(self, "Erro", resp.get("error", "Erro ao listar clientes"))

    def _preencher_tabela_clientes(self, clientes):
        """Preenche a tabela de clientes"""
        self.table_clientes.setRowCount(0)
        for cliente in clientes:
            row = self.table_clientes.rowCount()
            self.table_clientes.insertRow(row)

            # Obter saldo do cliente
            saldo_resp = self.controller.obter_saldo_cliente(cliente['id'])
            saldo = 0
            if saldo_resp.get("success"):
                saldo = saldo_resp.get("saldo", {}).get("saldo_pendente", 0)

            self.table_clientes.setItem(row, 0, QTableWidgetItem(str(cliente['id'])))
            self.table_clientes.setItem(row, 1, QTableWidgetItem(cliente['nome']))
            self.table_clientes.setItem(row, 2, QTableWidgetItem(f"R$ {saldo:.2f}"))

        self.table_clientes.resizeColumnsToContents()

    def _cliente_selecionado(self):
        """Executa quando um cliente é selecionado"""
        if self.table_clientes.selectedItems():
            row = self.table_clientes.currentRow()
            cliente_id = int(self.table_clientes.item(row, 0).text())

            resp = self.controller.obter_cliente(cliente_id)
            if resp.get("success"):
                cliente = resp.get("cliente")
                self.cliente_selecionado = cliente

                # Atualizar label com informações
                info_text = f"""
                ID: {cliente['id']}
                Nome: {cliente['nome']}
                Telefone: {cliente['telefone'] or 'N/A'}
                Email: {cliente['email'] or 'N/A'}
                Endereço: {cliente['endereco'] or 'N/A'}
                Cadastro: {format_date(cliente['data_cadastro'])}
                """
                self.label_cliente_info.setText(info_text.strip())

                # Carregar fiados do cliente
                self._carrregar_fiados_cliente(cliente_id)

                # Habilitar botões
                self.btn_editar_cliente.setEnabled(True)
                self.btn_deletar_cliente.setEnabled(True)
                self.btn_novo_fiado.setEnabled(True)

    def _carrregar_fiados_cliente(self, cliente_id: int):
        """Carrega fiados de um cliente"""
        resp = self.controller.listar_fiados_cliente(cliente_id, pendentes=False)
        if resp.get("success"):
            self._preencher_tabela_fiados(resp.get("fiados", []))
        else:
            QMessageBox.warning(self, "Erro", resp.get("error", "Erro ao carregar fiados"))

    def _preencher_tabela_fiados(self, fiados):
        """Preenche a tabela de fiados"""
        self.table_fiados.setRowCount(0)
        for fiado in fiados:
            row = self.table_fiados.rowCount()
            self.table_fiados.insertRow(row)

            self.table_fiados.setItem(row, 0, QTableWidgetItem(str(fiado['id'])))
            nome_produto = fiado.get('produto_nome') or ''
            self.table_fiados.setItem(row, 1, QTableWidgetItem(nome_produto))
            self.table_fiados.setItem(row, 2, QTableWidgetItem(str(fiado['quantidade'])))
            self.table_fiados.setItem(row, 3, QTableWidgetItem(f"R$ {fiado['valor_total']:.2f}"))
            self.table_fiados.setItem(row, 4, QTableWidgetItem(f"R$ {fiado['valor_pendente']:.2f}"))
            self.table_fiados.setItem(row, 5, QTableWidgetItem(format_date(fiado['data_fiado'])))

        self.table_fiados.resizeColumnsToContents()

    def _fiado_selecionado(self):
        """Executa quando um fiado é selecionado"""
        if self.table_fiados.selectedItems():
            self.btn_adicionar_pagamento.setEnabled(True)
            self.btn_deletar_fiado.setEnabled(True)
            self.btn_ver_pagamentos.setEnabled(True)

    def _abrir_dialog_novo_cliente(self):
        """Abre diálogo para criar novo cliente"""
        dialog = NovoClienteDialog(self)
        if dialog.exec():
            cliente_name = dialog.get_dados()
            resp = self.controller.criar_cliente(
                cliente_name['nome'],
                cliente_name['telefone'],
                cliente_name['email'],
                cliente_name['endereco']
            )
            if resp.get("success"):
                QMessageBox.information(self, "Sucesso", "Cliente criado com sucesso!")
                self._listar_clientes()
                self.input_pesquisa.clear()
            else:
                QMessageBox.warning(self, "Erro", resp.get("error"))

    def _abrir_dialog_editar_cliente(self):
        """Abre diálogo para editar cliente"""
        if not self.cliente_selecionado:
            return

        dialog = EditarClienteDialog(self, self.cliente_selecionado)
        if dialog.exec():
            dados = dialog.get_dados()
            resp = self.controller.atualizar_cliente(
                self.cliente_selecionado['id'],
                dados['nome'],
                dados['telefone'],
                dados['email'],
                dados['endereco']
            )
            if resp.get("success"):
                QMessageBox.information(self, "Sucesso", "Cliente atualizado com sucesso!")
                self._listar_clientes()
                # Reselecionar o cliente
                for i in range(self.table_clientes.rowCount()):
                    if int(self.table_clientes.item(i, 0).text()) == self.cliente_selecionado['id']:
                        self.table_clientes.selectRow(i)
                        break
            else:
                QMessageBox.warning(self, "Erro", resp.get("error"))

    def _deletar_cliente(self):
        """Deleta um cliente"""
        if not self.cliente_selecionado:
            return

        reply = QMessageBox.question(
            self, "Confirmar",
            f"Tem certeza que deseja deletar o cliente '{self.cliente_selecionado['nome']}'?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            resp = self.controller.deletar_cliente(self.cliente_selecionado['id'])
            if resp.get("success"):
                QMessageBox.information(self, "Sucesso", "Cliente deletado com sucesso!")
                self._listar_clientes()
                self.cliente_selecionado = None
                self.label_cliente_info.setText("Nenhum cliente selecionado")
                self.table_fiados.setRowCount(0)
                self.btn_editar_cliente.setEnabled(False)
                self.btn_deletar_cliente.setEnabled(False)
                self.btn_novo_fiado.setEnabled(False)
            else:
                QMessageBox.warning(self, "Erro", resp.get("error"))

    def _abrir_dialog_novo_fiado(self):
        """Abre diálogo para criar novo fiado"""
        if not self.cliente_selecionado:
            return

        dialog = NovoFiadoDialog(self, self.cliente_selecionado['id'], self.product_controller)
        if dialog.exec():
            dados = dialog.get_dados()
            resp = self.controller.criar_fiado(
                self.cliente_selecionado['id'],
                dados['produto_id'],
                dados['quantidade'],
                dados.get('produto_nome'),
                dados['observacao'],
                dados['data_vencimento']
            )
            if resp.get("success"):
                QMessageBox.information(self, "Sucesso", "Fiado criado com sucesso!")
                self._carrregar_fiados_cliente(self.cliente_selecionado['id'])
            else:
                QMessageBox.warning(self, "Erro", resp.get("error"))

    def _deletar_fiado(self):
        """Deleta um fiado"""
        if not self.table_fiados.selectedItems():
            return

        row = self.table_fiados.currentRow()
        fiado_id = int(self.table_fiados.item(row, 0).text())

        reply = QMessageBox.question(
            self, "Confirmar",
            "Tem certeza que deseja deletar este fiado?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            resp = self.controller.deletar_fiado(fiado_id)
            if resp.get("success"):
                QMessageBox.information(self, "Sucesso", "Fiado deletado com sucesso!")
                self._carrregar_fiados_cliente(self.cliente_selecionado['id'])
            else:
                QMessageBox.warning(self, "Erro", resp.get("error"))

    def _abrir_dialog_pagamento(self):
        """Abre diálogo para adicionar pagamento"""
        if not self.table_fiados.selectedItems():
            return

        row = self.table_fiados.currentRow()
        fiado_id = int(self.table_fiados.item(row, 0).text())
        valor_pendente = float(self.table_fiados.item(row, 4).text().replace("R$ ", ""))

        dialog = PagamentoFiadoDialog(self, fiado_id, valor_pendente)
        if dialog.exec():
            dados = dialog.get_dados()
            resp = self.controller.adicionar_pagamento(
                fiado_id,
                dados['valor'],
                dados['observacao']
            )
            if resp.get("success"):
                QMessageBox.information(self, "Sucesso", "Pagamento registrado com sucesso!")
                self._carrregar_fiados_cliente(self.cliente_selecionado['id'])
            else:
                QMessageBox.warning(self, "Erro", resp.get("error"))

    def _ver_pagamentos_fiado(self):
        """Visualiza pagamentos de um fiado"""
        if not self.table_fiados.selectedItems():
            return

        row = self.table_fiados.currentRow()
        fiado_id = int(self.table_fiados.item(row, 0).text())

        dialog = VisualizarPagamentosDialog(self, fiado_id, self.controller)
        dialog.exec()


class NovoClienteDialog(QDialog):
    """Diálogo para criar novo cliente"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Cliente")
        self.setModal(True)
        self.resize(400, 250)
        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)

        self.input_nome = QLineEdit()
        self.input_telefone = QLineEdit()
        self.input_email = QLineEdit()
        self.input_endereco = QLineEdit()

        layout.addRow("Nome *:", self.input_nome)
        layout.addRow("Telefone:", self.input_telefone)
        layout.addRow("Email:", self.input_email)
        layout.addRow("Endereço:", self.input_endereco)

        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")

        btn_salvar.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)

        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_cancelar)
        layout.addRow(btn_layout)

    def get_dados(self):
        return {
            'nome': self.input_nome.text(),
            'telefone': self.input_telefone.text(),
            'email': self.input_email.text(),
            'endereco': self.input_endereco.text()
        }


class EditarClienteDialog(QDialog):
    """Diálogo para editar cliente"""

    def __init__(self, parent=None, cliente=None):
        super().__init__(parent)
        self.setWindowTitle("Editar Cliente")
        self.setModal(True)
        self.resize(400, 250)
        self.cliente = cliente
        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)

        self.input_nome = QLineEdit()
        self.input_telefone = QLineEdit()
        self.input_email = QLineEdit()
        self.input_endereco = QLineEdit()

        if self.cliente:
            self.input_nome.setText(self.cliente['nome'])
            self.input_telefone.setText(self.cliente['telefone'] or '')
            self.input_email.setText(self.cliente['email'] or '')
            self.input_endereco.setText(self.cliente['endereco'] or '')

        layout.addRow("Nome *:", self.input_nome)
        layout.addRow("Telefone:", self.input_telefone)
        layout.addRow("Email:", self.input_email)
        layout.addRow("Endereço:", self.input_endereco)

        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")

        btn_salvar.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)

        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_cancelar)
        layout.addRow(btn_layout)

    def get_dados(self):
        return {
            'nome': self.input_nome.text(),
            'telefone': self.input_telefone.text(),
            'email': self.input_email.text(),
            'endereco': self.input_endereco.text()
        }


class NovoFiadoDialog(QDialog):
    """Diálogo para criar novo fiado"""

    def __init__(self, parent=None, cliente_id=None, product_controller=None):
        super().__init__(parent)
        self.setWindowTitle("Novo Fiado")
        self.setModal(True)
        self.resize(450, 300)
        self.cliente_id = cliente_id
        self.product_controller = product_controller
        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)

        # ComboBox para produtos
        self.combo_produto = QComboBox()
        self._carrregar_produtos()

        # campo livre para nome quando produto faltando
        self.input_produto_nome = QLineEdit()
        self.input_produto_nome.setPlaceholderText("Nome do produto (se não listado)")
        self.input_produto_nome.hide()

        self.input_quantidade = QSpinBox()
        self.input_quantidade.setMinimum(1)
        self.input_quantidade.setMaximum(999)

        self.input_observacao = QTextEdit()
        self.input_observacao.setMaximumHeight(60)

        self.input_data_vencimento = QDateEdit()
        self.input_data_vencimento.setDate(QDate.currentDate())
        self.input_data_vencimento.setCalendarPopup(True)

        layout.addRow("Produto *:", self.combo_produto)
        layout.addRow("Nome do produto:", self.input_produto_nome)
        layout.addRow("Quantidade *:", self.input_quantidade)
        layout.addRow("Data de Vencimento:", self.input_data_vencimento)
        layout.addRow("Observação:", self.input_observacao)

        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Salvar")
        btn_cancelar = QPushButton("Cancelar")

        btn_salvar.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)

        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_cancelar)
        layout.addRow(btn_layout)

        # conectar sinal após criar todos os elementos
        self.combo_produto.currentIndexChanged.connect(self._produto_changed)

        # definir visibilidade inicial do campo de nome
        self._produto_changed()

    def _produto_changed(self):
        """Mostra ou esconde o campo de nome livre dependendo da seleção"""
        if self.combo_produto.currentData() is None:
            self.input_produto_nome.show()
        else:
            self.input_produto_nome.hide()
            self.input_produto_nome.clear()

    def _carrregar_produtos(self):
        """Carrega lista de produtos"""
        # inserir opcao para "outro produto" que nao esteja no cadastro
        self.combo_produto.addItem("-- Outro produto --", None)
        if self.product_controller:
            produtos = self.product_controller.list_products()
            if isinstance(produtos, list):
                for produto in produtos:
                    self.combo_produto.addItem(produto['nome'], produto['id'])

    def get_dados(self):
        # se o usuario escolheu a opcao de outro produto (produto_id None),
        # retornamos tambem o nome preenchido no campo livre
        produto_id = self.combo_produto.currentData()
        dados = {
            'produto_id': produto_id,
            'quantidade': self.input_quantidade.value(),
            'observacao': self.input_observacao.toPlainText(),
            'data_vencimento': self.input_data_vencimento.date().toString("yyyy-MM-dd") if self.input_data_vencimento.date() else None
        }
        if produto_id is None:
            dados['produto_nome'] = self.input_produto_nome.text().strip() or None
        else:
            # garantir que chave exista para facilitar uso no controller
            dados['produto_nome'] = None
        return dados


class PagamentoFiadoDialog(QDialog):
    """Diálogo para adicionar pagamento a um fiado"""

    def __init__(self, parent=None, fiado_id=None, valor_pendente=0):
        super().__init__(parent)
        self.setWindowTitle("Adicionar Pagamento")
        self.setModal(True)
        self.resize(400, 200)
        self.fiado_id = fiado_id
        self.valor_pendente = valor_pendente
        self._build_ui()

    def _build_ui(self):
        layout = QFormLayout(self)

        label_pendente = QLabel(f"Valor Pendente: R$ {self.valor_pendente:.2f}")
        layout.addRow(label_pendente)

        self.input_valor = QDoubleSpinBox()
        self.input_valor.setMinimum(0.01)
        self.input_valor.setMaximum(self.valor_pendente)
        self.input_valor.setValue(self.valor_pendente)
        self.input_valor.setDecimals(2)

        self.input_observacao = QTextEdit()
        self.input_observacao.setMaximumHeight(60)

        layout.addRow("Valor a Pagar *:", self.input_valor)
        layout.addRow("Observação:", self.input_observacao)

        btn_layout = QHBoxLayout()
        btn_salvar = QPushButton("Confirmar Pagamento")
        btn_cancelar = QPushButton("Cancelar")

        btn_salvar.clicked.connect(self.accept)
        btn_cancelar.clicked.connect(self.reject)

        btn_layout.addWidget(btn_salvar)
        btn_layout.addWidget(btn_cancelar)
        layout.addRow(btn_layout)

    def get_dados(self):
        return {
            'valor': self.input_valor.value(),
            'observacao': self.input_observacao.toPlainText()
        }


class VisualizarPagamentosDialog(QDialog):
    """Diálogo para visualizar pagamentos de um fiado"""

    def __init__(self, parent=None, fiado_id=None, controller=None):
        super().__init__(parent)
        self.setWindowTitle("Pagamentos do Fiado")
        self.setModal(True)
        self.resize(600, 400)
        self.fiado_id = fiado_id
        self.controller = controller
        self._build_ui()
        self._carregar_pagamentos()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        self.table_pagamentos = QTableWidget(0, 3)
        self.table_pagamentos.setHorizontalHeaderLabels(["Valor", "Data", "Observação"])
        layout.addWidget(self.table_pagamentos)

        btn_fechar = QPushButton("Fechar")
        btn_fechar.clicked.connect(self.close)
        layout.addWidget(btn_fechar)

    def _carregar_pagamentos(self):
        """Carrega os pagamentos do fiado"""
        if self.controller:
            resp = self.controller.obter_pagamentos_fiado(self.fiado_id)
            if resp.get("success"):
                pagamentos = resp.get("pagamentos", [])
                self.table_pagamentos.setRowCount(0)
                for pagamento in pagamentos:
                    row = self.table_pagamentos.rowCount()
                    self.table_pagamentos.insertRow(row)

                    self.table_pagamentos.setItem(row, 0, QTableWidgetItem(f"R$ {pagamento['valor_pago']:.2f}"))
                    self.table_pagamentos.setItem(row, 1, QTableWidgetItem(format_date(pagamento['data_pagamento'])))
                    self.table_pagamentos.setItem(row, 2, QTableWidgetItem(pagamento['observacao'] or ''))

                self.table_pagamentos.resizeColumnsToContents()
