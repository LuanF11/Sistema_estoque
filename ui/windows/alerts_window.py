from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QTableWidget, QTableWidgetItem, QGroupBox, QTabWidget
)
from PySide6.QtGui import QColor, QIcon, QFont
from PySide6.QtCore import Qt, QSize
from datetime import datetime, date
from utils.dates import format_date

from controllers.product_controller import ProductController


class AlertsWindow(QWidget):
    
    def __init__(self):
        super().__init__()
        
        self.controller = ProductController()
        self.setWindowTitle("Dashboard de Alertas")
        
        self._build_ui()
        self.load_alerts()
    
    def _build_ui(self):
        layout = QVBoxLayout(self)
        
        summary_layout = QHBoxLayout()
        
        self.card_expired = self._create_card("Produtos Vencidos", "0", QColor(64, 64, 64))
        self.card_expiring = self._create_card("Próximos do Vencimento", "0", QColor(255, 0, 0))
        self.card_low_stock = self._create_card("Estoque Baixo", "0", QColor(255, 255, 0))
        
        summary_layout.addWidget(self.card_expired)
        summary_layout.addWidget(self.card_expiring)
        summary_layout.addWidget(self.card_low_stock)
        
        layout.addLayout(summary_layout)
        
        self.tabs = QTabWidget()
        
        self.table_expired = self._create_table()
        self.table_expiring = self._create_table()
        self.table_low_stock = self._create_table()
        
        self.tabs.addTab(self.table_expired, "⚫Vencidos")
        self.tabs.addTab(self.table_expiring, "🔴 Próximos do Vencimento")
        self.tabs.addTab(self.table_low_stock, "🟡 Estoque Baixo")
        
        layout.addWidget(self.tabs)
        
        btn_refresh = QPushButton("🔄 Atualizar")
        btn_refresh.clicked.connect(self.load_alerts)
        layout.addWidget(btn_refresh)
    
    def _create_card(self, title, count, color):
        """Cria um card de resumo com título, contagem e cor"""
        widget = QGroupBox(title)
        layout = QVBoxLayout()
        
        label_count = QLabel(count)
        label_count.setFont(QFont("Arial", 24, QFont.Bold))
        label_count.setAlignment(Qt.AlignCenter)
        label_count.setStyleSheet(f"color: {color.name()}; padding: 20px;")
        
        layout.addWidget(label_count)
        widget.setLayout(layout)
        
        # Armazenar a label para atualizar depois
        widget.label_count = label_count
        
        return widget
    
    def _create_table(self):
        """Cria uma tabela padrão para os alertas"""
        table = QTableWidget()
        table.setColumnCount(6)
        table.setHorizontalHeaderLabels([
            "ID", "Nome", "Quantidade", "Estoque Mín.", 
            "Detalhes do Aviso", "Tags"
        ])
        table.resizeColumnsToContents()
        return table
    
    def load_alerts(self):
        """Carrega todos os alertas e preenche as tabelas"""
        products = self.controller.list_products()
        
        expired_products = []
        expiring_products = []
        low_stock_products = []
        
        for product in products:
            alertas = self.controller.service.get_product_alert_status(product, 7)
            
            if "Vencido" in alertas:
                expired_products.append(product)
            if "Perto do vencimento" in alertas:
                expiring_products.append(product)
            if "Estoque baixo" in alertas:
                low_stock_products.append(product)
        
        # Atualizar cards
        self.card_expired.label_count.setText(str(len(expired_products)))
        self.card_expiring.label_count.setText(str(len(expiring_products)))
        self.card_low_stock.label_count.setText(str(len(low_stock_products)))
        
        # Preencher tabelas
        self._populate_table(self.table_expired, expired_products, "expired")
        self._populate_table(self.table_expiring, expiring_products, "expiring")
        self._populate_table(self.table_low_stock, low_stock_products, "low_stock")
    
    def _populate_table(self, table, products, alert_type):
        """Preenche uma tabela com os produtos e detalhes do alerta"""
        table.setRowCount(len(products))
        
        for row, product in enumerate(products):
            table.setItem(row, 0, QTableWidgetItem(str(product["id"])))
            table.setItem(row, 1, QTableWidgetItem(product["nome"]))
            table.setItem(row, 2, QTableWidgetItem(str(product["quantidade"])))
            table.setItem(row, 3, QTableWidgetItem(str(product.get("estoque_minimo", 5))))
            details = self._get_alert_details(product, alert_type)
            table.setItem(row, 4, QTableWidgetItem(details))
            table.setItem(row, 5, QTableWidgetItem(product.get("tags", "")))
            
            # Colorir a linha baseado no tipo de alerta
            if alert_type == "expired":
                color = QColor(64, 64, 64, 50)  # Cinza escuro
            elif alert_type == "expiring":
                color = QColor(255, 0, 0, 50)  # Vermelho
            else:  # low_stock
                color = QColor(255, 255, 0, 50)  # Amarelo
            
            for col in range(table.columnCount()):
                item = table.item(row, col)
                if item:
                    item.setBackground(color)
        
        table.resizeColumnsToContents()
    
    def _get_alert_details(self, product, alert_type):
        """Retorna uma string com detalhes do alerta"""
        if alert_type == "expired":
            if product["data_validade"]:
                validade_date = datetime.strptime(product["data_validade"], "%Y-%m-%d").date()
                days_passed = (date.today() - validade_date).days
                return f"Vencido há {days_passed} dias"
            return "Vencido"
        
        elif alert_type == "expiring":
            if product["data_validade"]:
                validade_date = datetime.strptime(product["data_validade"], "%Y-%m-%d").date()
                days_left = (validade_date - date.today()).days
                return f"Vence em {days_left} dias ({format_date(product['data_validade'])})"
            return "Próximo do vencimento"
        
        else:  # low_stock
            estoque_minimo = product.get("estoque_minimo", 5)
            quantidade = product.get("quantidade", 0)
            falta = estoque_minimo - quantidade
            return f"Faltam {falta} unidades para atingir o mínimo"
