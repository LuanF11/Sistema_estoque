from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QGroupBox, QGridLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QDateEdit
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QFont, QColor

from repositories.caixa_repository import CaixaRepository


class CaixaDashboardWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.caixa_repo = CaixaRepository()
        self._build_ui()
        self.atualizar_dashboard()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        titulo = QLabel("Resumo de Caixas")
        titulo_font = QFont()
        titulo_font.setPointSize(16)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)

        # Cards de resumo
        resumo_layout = QGridLayout()
        resumo_layout.setSpacing(15)

        # Card 1: Total de Caixas
        self.card_total = self._criar_card(
            "📊 Total de Caixas",
            "0",
            "#3498db"
        )
        resumo_layout.addWidget(self.card_total, 0, 0)

        # Card 2: Caixas Abertos
        self.card_abertos = self._criar_card(
            "🟢 Caixas Abertos",
            "0",
            "#27ae60"
        )
        resumo_layout.addWidget(self.card_abertos, 0, 1)

        # Card 3: Caixas Fechados
        self.card_fechados = self._criar_card(
            "🔴 Caixas Fechados",
            "0",
            "#e74c3c"
        )
        resumo_layout.addWidget(self.card_fechados, 0, 2)

        # Card 4: Soma Aberturas
        self.card_soma_aberturas = self._criar_card(
            "💰 Soma de Aberturas",
            "R$ 0,00",
            "#2ecc71"
        )
        resumo_layout.addWidget(self.card_soma_aberturas, 1, 0)

        # Card 5: Soma Fechamentos
        self.card_soma_fechamentos = self._criar_card(
            "💵 Soma de Fechamentos",
            "R$ 0,00",
            "#9b59b6"
        )
        resumo_layout.addWidget(self.card_soma_fechamentos, 1, 1)

        # Card 6: Diferença Total
        self.card_diferenca = self._criar_card(
            "📈 Diferença Total",
            "R$ 0,00",
            "#f39c12"
        )
        resumo_layout.addWidget(self.card_diferenca, 1, 2)

        layout.addLayout(resumo_layout)

        # Tabela com detalhes
        layout.addWidget(QLabel("Histórico Detalhado"))
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Data", "Status", "Abertura", "Fechamento", "Diferença", "% Var."
        ])
        layout.addWidget(self.table)

        # Botão de atualização
        btn_atualizar = QPushButton("Atualizar")
        btn_atualizar.clicked.connect(self.atualizar_dashboard)
        layout.addWidget(btn_atualizar)

    def _criar_card(self, titulo, valor, cor):
        """Cria um card visual com título, valor e cor"""
        card = QGroupBox()
        layout = QVBoxLayout()

        titulo_label = QLabel(titulo)
        titulo_label.setFont(QFont("Arial", 10, QFont.Bold))
        titulo_label.setStyleSheet(f"color: {cor};")

        valor_label = QLabel(valor)
        valor_font = QFont("Arial", 16, QFont.Bold)
        valor_label.setFont(valor_font)
        valor_label.setStyleSheet(f"color: {cor};")

        layout.addWidget(titulo_label)
        layout.addWidget(valor_label)
        layout.setContentsMargins(15, 15, 15, 15)

        card.setLayout(layout)
        card.setStyleSheet(f"QGroupBox {{ background-color: #f8f9fa; padding: 10px; border-radius: 5px; border: 2px solid {cor}; border-style: solid; }}")

        # Guardar referência para atualizar depois
        card.valor_label = valor_label
        return card

    def atualizar_dashboard(self):
        """Atualiza todos os dados do dashboard"""
        caixas = self.caixa_repo.get_all()

        # Cálculos
        total = len(caixas)
        abertos = sum(1 for c in caixas if c["status"] == "ABERTO")
        fechados = total - abertos

        soma_aberturas = sum(c["valor_abertura"] for c in caixas)
        soma_fechamentos = sum(c["valor_fechamento"] or 0 for c in caixas)
        diferenca_total = soma_fechamentos - soma_aberturas

        # Atualizar cards
        self.card_total.valor_label.setText(str(total))
        self.card_abertos.valor_label.setText(str(abertos))
        self.card_fechados.valor_label.setText(str(fechados))
        self.card_soma_aberturas.valor_label.setText(f"R$ {soma_aberturas:.2f}")
        self.card_soma_fechamentos.valor_label.setText(f"R$ {soma_fechamentos:.2f}")
        
        cor_diferenca = "#27ae60" if diferenca_total >= 0 else "#e74c3c"
        self.card_diferenca.valor_label.setStyleSheet(f"color: {cor_diferenca};")
        self.card_diferenca.valor_label.setText(f"R$ {diferenca_total:.2f}")

        # Preencher tabela
        self.table.setRowCount(len(caixas))

        for row, caixa in enumerate(caixas):
            self.table.setItem(row, 0, QTableWidgetItem(str(caixa["id"])))
            self.table.setItem(row, 1, QTableWidgetItem(caixa["data"]))
            self.table.setItem(row, 2, QTableWidgetItem(caixa["status"]))
            self.table.setItem(row, 3, QTableWidgetItem(f"R$ {caixa['valor_abertura']:.2f}"))

            if caixa["valor_fechamento"]:
                self.table.setItem(row, 4, QTableWidgetItem(f"R$ {caixa['valor_fechamento']:.2f}"))
                diferenca = caixa["valor_fechamento"] - caixa["valor_abertura"]
                self.table.setItem(row, 5, QTableWidgetItem(f"R$ {diferenca:.2f}"))
                
                # Percentual de variação
                if caixa["valor_abertura"] != 0:
                    pct = (diferenca / caixa["valor_abertura"]) * 100
                    self.table.setItem(row, 6, QTableWidgetItem(f"{pct:.1f}%"))
                else:
                    self.table.setItem(row, 6, QTableWidgetItem("N/A"))

                # Colorir linha conforme resultado
                cor = QColor(200, 255, 200, 100) if diferenca >= 0 else QColor(255, 200, 200, 100)
            else:
                self.table.setItem(row, 4, QTableWidgetItem("-"))
                self.table.setItem(row, 5, QTableWidgetItem("-"))
                self.table.setItem(row, 6, QTableWidgetItem("-"))
                cor = QColor(220, 220, 220, 100)

            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item:
                    item.setBackground(cor)
