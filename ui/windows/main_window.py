from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QMenuBar, QMenu, QStackedWidget
)
from PySide6.QtCore import Qt

from ui.windows.home_screen import HomeScreen
from ui.windows.product_window import ProductWindow
from ui.windows.tag_window import TagWindow
from ui.windows.stock_window import StockWindow
from ui.windows.report_window import ReportWindow
from ui.windows.alerts_window import AlertsWindow
from ui.windows.caixa_window import CaixaWindow
from ui.windows.caixa_dashboard_window import CaixaDashboardWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Sistema de Controle de Estoque")
        self.setMinimumSize(1000, 600)

        self._create_menu()
        self._create_central_area()

    def _create_menu(self):
        menu_bar = QMenuBar(self)

        menu_inicio = QMenu("Início", self)
        menu_caixa = QMenu("Caixa", self)
        menu_produtos = QMenu("Produtos", self)
        menu_estoque = QMenu("Estoque", self)
        menu_relatorios = QMenu("Relatórios", self)

        menu_bar.addMenu(menu_inicio)
        menu_bar.addMenu(menu_caixa)
        menu_bar.addMenu(menu_produtos)
        menu_bar.addMenu(menu_estoque)
        menu_bar.addMenu(menu_relatorios)

        self.setMenuBar(menu_bar)

        self.menu_inicio = menu_inicio
        self.menu_caixa = menu_caixa
        self.menu_produtos = menu_produtos
        self.menu_estoque = menu_estoque
        self.menu_relatorios = menu_relatorios

        # Menu Início
        action_home = menu_inicio.addAction("Controle de Caixa")
        action_home.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_screen))

        # Menu Caixa
        action_gerenciar_caixa = menu_caixa.addAction("Gerenciar Caixas")
        action_gerenciar_caixa.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.caixa_window))

        # Menu Produtos
        action_produtos = menu_produtos.addAction("Gerenciar Produtos")
        action_produtos.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.product_window))

        action_tags = menu_produtos.addAction("Gerenciar Tags")
        action_tags.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.tag_window))

        action_stock = menu_produtos.addAction("Movimentação de Estoque")
        action_stock.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.stock_window))

        # Menu Estoque
        action_alerts = menu_estoque.addAction("Dashboard de Alertas")
        action_alerts.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.alerts_window))

        # Menu Relatórios
        action_report = menu_relatorios.addAction("Vendas e Lucro")
        action_report.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.report_window))

        action_caixa_dashboard = menu_relatorios.addAction("Resumo de Caixas")
        action_caixa_dashboard.triggered.connect(lambda: self.stacked_widget.setCurrentWidget(self.caixa_dashboard_window))

    def _create_central_area(self):
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        self.home_screen = HomeScreen()
        self.stacked_widget.addWidget(self.home_screen)

        self.caixa_dashboard_window = CaixaDashboardWindow()
        self.stacked_widget.addWidget(self.caixa_dashboard_window)

        self.caixa_window = CaixaWindow()
        self.stacked_widget.addWidget(self.caixa_window)

        self.product_window = ProductWindow()
        self.stacked_widget.addWidget(self.product_window)

        self.tag_window = TagWindow()
        self.stacked_widget.addWidget(self.tag_window)

        self.stock_window = StockWindow()
        self.stacked_widget.addWidget(self.stock_window)

        self.alerts_window = AlertsWindow()
        self.stacked_widget.addWidget(self.alerts_window)

        self.report_window = ReportWindow()
        self.stacked_widget.addWidget(self.report_window)

        # Mostra home screen por padrão
        self.stacked_widget.setCurrentWidget(self.home_screen)
