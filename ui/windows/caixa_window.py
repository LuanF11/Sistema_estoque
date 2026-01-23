from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QTableWidget,
    QTableWidgetItem, QLabel, QMessageBox
)
from PySide6.QtGui import QColor

from controllers.caixa_controller import CaixaController


class CaixaWindow(QWidget):

    def __init__(self):
        super().__init__()

        self.controller = CaixaController()

        self._build_ui()
        self.load_caixas()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Barra superior
        top_bar = QHBoxLayout()

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Buscar caixa por ID ou data")

        btn_search = QPushButton("Buscar")
        btn_search.clicked.connect(self.search_caixas)

        btn_new = QPushButton("Novo Caixa")
        btn_new.clicked.connect(self.new_caixa)

        self.btn_delete = QPushButton("Deletar")
        self.btn_delete.setEnabled(False)
        self.btn_delete.setToolTip("Selecione um caixa para deletar")
        self.btn_delete.clicked.connect(self.delete_caixa)

        top_bar.addWidget(QLabel("Caixas"))
        top_bar.addStretch()
        top_bar.addWidget(self.search_input)
        top_bar.addWidget(btn_search)
        top_bar.addWidget(btn_new)
        top_bar.addWidget(self.btn_delete)

        # Tabela
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "ID", "Data", "Status", "Valor Abertura",
            "Valor Fechamento", "Diferença"
        ])

        layout.addLayout(top_bar)
        layout.addWidget(self.table)

        self.table.cellDoubleClicked.connect(self.edit_caixa)
        self.table.selectionModel().selectionChanged.connect(self.on_selection_changed)

    def new_caixa(self):
        valor, ok = self._get_valor_abertura()
        if ok and valor is not None:
            result = self.controller.abrir_caixa(valor)
            if result.get("success"):
                self.load_caixas()
                QMessageBox.information(self, "Sucesso", result.get("message", "Caixa aberto com sucesso"))
            else:
                QMessageBox.warning(self, "Erro", result.get("error", "Erro ao abrir caixa"))

    def _get_valor_abertura(self):
        from PySide6.QtWidgets import QInputDialog
        valor, ok = QInputDialog.getDouble(
            self,
            "Novo Caixa",
            "Valor de abertura:",
            0.0,
            0.0,
            999999.99,
            2
        )
        return valor, ok

    def edit_caixa(self, row, column):
        caixa_id = int(self.table.item(row, 0).text())
        status = self.table.item(row, 2).text()

        if status == "FECHADO":
            QMessageBox.information(self, "Info", "Não é possível editar um caixa fechado")
            return

        valor, ok = self._get_valor_fechamento()
        if ok and valor is not None:
            result = self.controller.fechar_caixa(caixa_id, valor)
            if result.get("success"):
                self.load_caixas()
                QMessageBox.information(
                    self,
                    "Sucesso",
                    f"{result.get('message')}\nAbertura: R$ {result['valor_abertura']:.2f}\nFechamento: R$ {result['valor_fechamento']:.2f}\nDiferença: R$ {result['diferenca']:.2f}"
                )
            else:
                QMessageBox.warning(self, "Erro", result.get("error", "Erro ao fechar caixa"))

    def _get_valor_fechamento(self):
        from PySide6.QtWidgets import QInputDialog
        valor, ok = QInputDialog.getDouble(
            self,
            "Fechar Caixa",
            "Valor de fechamento:",
            0.0,
            0.0,
            999999.99,
            2
        )
        return valor, ok

    def delete_caixa(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if not selected_rows:
            QMessageBox.warning(self, "Aviso", "Selecione um caixa para deletar")
            return

        row = selected_rows[0].row()
        caixa_id = int(self.table.item(row, 0).text())
        status = self.table.item(row, 2).text()
        data = self.table.item(row, 1).text()

        if status == "FECHADO":
            QMessageBox.warning(self, "Aviso", "Não é possível deletar um caixa fechado")
            return

        reply = QMessageBox.question(
            self,
            "Confirmar Deleção",
            f"Tem certeza que deseja deletar o caixa de {data}?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            self.controller.service.repository.delete(caixa_id)
            self.load_caixas()
            QMessageBox.information(self, "Sucesso", "Caixa deletado com sucesso")

    def on_selection_changed(self):
        """Habilita/desabilita o botão de deletar conforme a seleção"""
        has_selection = len(self.table.selectionModel().selectedRows()) > 0
        self.btn_delete.setEnabled(has_selection)

    def load_caixas(self):
        caixas = self.controller.service.repository.get_all()
        self.table.setRowCount(len(caixas))

        for row, caixa in enumerate(caixas):
            self.table.setItem(row, 0, QTableWidgetItem(str(caixa["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(caixa["data"]))
            self.table.setItem(row, 2, QTableWidgetItem(caixa["status"]))
            self.table.setItem(row, 3, QTableWidgetItem(f"R$ {caixa['valor_abertura']:.2f}"))

            valor_fechamento = caixa.get("valor_fechamento")
            if valor_fechamento is not None:
                self.table.setItem(row, 4, QTableWidgetItem(f"R$ {valor_fechamento:.2f}"))
                diferenca = valor_fechamento - caixa["valor_abertura"]
                self.table.setItem(row, 5, QTableWidgetItem(f"R$ {diferenca:.2f}"))
            else:
                self.table.setItem(row, 4, QTableWidgetItem("-"))
                self.table.setItem(row, 5, QTableWidgetItem("-"))

            # Colorir conforme status
            if caixa["status"] == "FECHADO":
                color = QColor(200, 200, 200, 100)  # Cinza
            else:
                color = QColor(200, 255, 200, 100)  # Verde claro

            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(color)

    def search_caixas(self):
        termo = self.search_input.text().lower()
        if not termo:
            self.load_caixas()
            return

        caixas = self.controller.service.repository.get_all()
        filtrados = [c for c in caixas if termo in str(c["id"]) or termo in c["data"]]

        self.table.setRowCount(len(filtrados))

        for row, caixa in enumerate(filtrados):
            self.table.setItem(row, 0, QTableWidgetItem(str(caixa["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(caixa["data"]))
            self.table.setItem(row, 2, QTableWidgetItem(caixa["status"]))
            self.table.setItem(row, 3, QTableWidgetItem(f"R$ {caixa['valor_abertura']:.2f}"))

            valor_fechamento = caixa.get("valor_fechamento")
            if valor_fechamento is not None:
                self.table.setItem(row, 4, QTableWidgetItem(f"R$ {valor_fechamento:.2f}"))
                diferenca = valor_fechamento - caixa["valor_abertura"]
                self.table.setItem(row, 5, QTableWidgetItem(f"R$ {diferenca:.2f}"))
            else:
                self.table.setItem(row, 4, QTableWidgetItem("-"))
                self.table.setItem(row, 5, QTableWidgetItem("-"))

            # Colorir conforme status
            if caixa["status"] == "FECHADO":
                color = QColor(200, 200, 200, 100)
            else:
                color = QColor(200, 255, 200, 100)

            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(color)
