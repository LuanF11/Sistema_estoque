from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QGroupBox, QGridLayout, QTableWidget,
    QTableWidgetItem, QPushButton, QDateEdit
)
from PySide6.QtCore import QDate
from PySide6.QtGui import QFont, QColor

from repositories.caixa_repository import CaixaRepository
from repositories.stock_repository import StockRepository
from repositories.caixa_movimentacao_repository import CaixaMovimentacaoRepository
from repositories.product_repository import ProductRepository


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

        # Tabela de Histórico de Caixas (resumo por dia)
        layout.addWidget(QLabel("Histórico Detalhado"))
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "ID", "Data", "Status", "Abertura", "Fechamento", "Diferença", "% Var."
        ])
        layout.addWidget(self.table)

        # Área de Movimentações por Data
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(QLabel("Selecione a data:"))
        self.date_edit = QDateEdit()
        self.date_edit.setDate(QDate.currentDate())
        self.date_edit.setCalendarPopup(True)
        controls_layout.addWidget(self.date_edit)

        btn_carregar = QPushButton("Carregar Movimentos")
        btn_carregar.clicked.connect(self.carregar_movimentacoes)
        controls_layout.addWidget(btn_carregar)
        controls_layout.addStretch()
        layout.addLayout(controls_layout)

        layout.addWidget(QLabel("Movimentações do Dia"))
        self.mov_table = QTableWidget()
        self.mov_table.setColumnCount(6)
        self.mov_table.setHorizontalHeaderLabels([
            "Tipo", "Hora", "Item/Categoria", "Quantidade", "Valor (R$)", "Descrição"
        ])
        layout.addWidget(self.mov_table)

        # Botão de atualização do dashboard (caixas)
        btn_atualizar = QPushButton("Atualizar Resumo")
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
    
    def carregar_movimentacoes(self):
        """Carrega movimentações (produtos + avulsos) para a data selecionada e popula a tabela."""
        target_qdate = self.date_edit.date()
        target_date = target_qdate.toString("yyyy-MM-dd")

        stock_repo = StockRepository()
        mov_repo = CaixaMovimentacaoRepository()
        product_repo = ProductRepository()

        # Movimentações de produtos (SAIDA/ENTRADA)
        movimentos = stock_repo.list_by_period(target_date, target_date) or []

        rows = []
        for m in movimentos:
            # m expected: (id, produto_id, tipo, quantidade, data_movimentacao, observacao)
            produto_id = m[1]
            tipo = m[2]
            quantidade = m[3]
            data_mov = m[4]
            observacao = m[5] or ""

            prod = product_repo.get_by_id(produto_id) or {}
            nome = prod.get("nome", f"Produto #{produto_id}")
            valor_unit = prod.get("valor_venda", 0) or 0
            valor_total = quantidade * valor_unit

            hora = data_mov.split(" ")[-1] if isinstance(data_mov, str) else str(data_mov)

            rows.append(("Produto", hora, nome, str(quantidade), f"{valor_total:.2f}", observacao))

        # Movimentações avulsas de caixa
        avulsos = mov_repo.list_by_date(target_date) or []
        for a in avulsos:
            # a expected: (id, caixa_id, tipo, valor, categoria, descricao, data_movimentacao)
            tipo = a[2]
            valor = a[3]
            categoria = a[4] or ""
            descricao = a[5] or ""
            data_mov = a[6]
            hora = data_mov.split(" ")[-1] if isinstance(data_mov, str) else str(data_mov)

            rows.append((f"Avulso ({tipo})", hora, categoria, "-", f"{valor:.2f}", descricao))

        # Ordena por hora (assumindo formato yyyy-MM-dd HH:MM:SS)
        try:
            rows.sort(key=lambda r: r[1])
        except Exception:
            pass

        # Preenche tabela
        self.mov_table.setRowCount(len(rows))
        for i, r in enumerate(rows):
            for c, val in enumerate(r):
                self.mov_table.setItem(i, c, QTableWidgetItem(val))

    def refresh(self):
        """Recarrega o dashboard quando a aba fica visível."""
        self.atualizar_dashboard()