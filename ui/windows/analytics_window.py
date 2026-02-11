from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QScrollArea,
    QGroupBox, QTabWidget, QMessageBox, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from services.analytics_service import AnalyticsService
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AnalyticsWindow(QWidget):
    """Dashboard com análises avançadas de dados"""

    def __init__(self):
        super().__init__()
        self.service = AnalyticsService()
        self._build_ui()
        self._load_data()

    def showEvent(self, event):
        """Atualiza dados quando a tela fica visível."""
        super().showEvent(event)
        self._load_data()

    def _build_ui(self):
        """Construir interface do dashboard"""
        layout = QVBoxLayout(self)

        # Título e botão de atualizar
        title_layout = QHBoxLayout()
        title = QLabel("Dashboard de Análises")

        # Abas principais
        tabs = QTabWidget()
        
        # Aba 1: Visão Geral
        tabs.addTab(self._create_overview_tab(), "Visão Geral")
        
        # Aba 2: Vendas e Lucro
        tabs.addTab(self._create_sales_tab(), "Vendas & Lucro")
        
        # Aba 3: Estoque
        tabs.addTab(self._create_stock_tab(), "Estoque")
        
        # Aba 4: Análise de Produtos
        tabs.addTab(self._create_products_tab(), "Análise de Produtos")

        layout.addWidget(tabs)

    def _create_overview_tab(self):
        """Aba de visão geral"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Estatísticas principais
        stats_layout = QHBoxLayout()
        
        self.label_produtos = self._create_stat_box("Produtos Ativos", "0")
        self.label_itens = self._create_stat_box("Itens em Estoque", "0")
        self.label_vendas = self._create_stat_box("Total de Vendas", "0")
        self.label_dias = self._create_stat_box("Dias com Vendas", "0")
        self.label_fiados = self._create_stat_box("Fiados Abertos (R$)", "R$ 0,00")

        stats_layout.addWidget(self.label_produtos)
        stats_layout.addWidget(self.label_itens)
        stats_layout.addWidget(self.label_vendas)
        stats_layout.addWidget(self.label_dias)
        stats_layout.addWidget(self.label_fiados)

        layout.addLayout(stats_layout)

        # Gráfico de vendas vs lucro
        self.figure_sales = Figure(figsize=(12, 4), dpi=100)
        self.canvas_sales = FigureCanvas(self.figure_sales)
        layout.addWidget(QLabel("Tendência de Vendas (Últimos 30 dias)"))
        layout.addWidget(self.canvas_sales)

        return widget

    def _create_sales_tab(self):
        """Aba de vendas e lucro"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Top produtos
        group = QGroupBox("Top 5 Produtos Mais Vendidos")
        group_layout = QVBoxLayout(group)

        self.table_top_produtos = QTableWidget(0, 5)
        self.table_top_produtos.setHorizontalHeaderLabels([
            "Produto", "Qtd Vendida", "Faturamento", "Lucro", "Margem"
        ])
        self.table_top_produtos.setColumnWidth(0, 200)
        group_layout.addWidget(self.table_top_produtos)
        layout.addWidget(group)

        # Desempenho por categoria
        group2 = QGroupBox("Desempenho por Categoria")
        group2_layout = QVBoxLayout(group2)

        self.figure_categories = Figure(figsize=(12, 4), dpi=100)
        self.canvas_categories = FigureCanvas(self.figure_categories)
        group2_layout.addWidget(self.canvas_categories)
        layout.addWidget(group2)
        

        return widget

    def _create_stock_tab(self):
        """Aba de estoque"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Métricas de estoque
        metrics_layout = QHBoxLayout()
        self.label_valor_custo = self._create_stat_box("Valor (Custo)", "R$ 0,00")
        self.label_valor_venda = self._create_stat_box("Valor (Venda)", "R$ 0,00")
        self.label_margem_total = self._create_stat_box("Margem Potencial", "R$ 0,00")

        metrics_layout.addWidget(self.label_valor_custo)
        metrics_layout.addWidget(self.label_valor_venda)
        metrics_layout.addWidget(self.label_margem_total)

        layout.addLayout(metrics_layout)

        # Distribuição de estoque por categoria
        self.figure_stock = Figure(figsize=(12, 4), dpi=100)
        self.canvas_stock = FigureCanvas(self.figure_stock)
        layout.addWidget(QLabel("Distribuição de Estoque por Categoria"))
        layout.addWidget(self.canvas_stock)

        return widget

    def _create_products_tab(self):
        """Aba de análise de produtos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        tabs = QTabWidget()

        # Margem de lucro
        tab1 = QWidget()
        tab1_layout = QVBoxLayout(tab1)
        self.table_margens = QTableWidget(0, 5)
        self.table_margens.setHorizontalHeaderLabels([
            "Produto", "Custo", "Venda", "Margem %", "Lucro Total"
        ])
        tab1_layout.addWidget(self.table_margens)
        tabs.addTab(tab1, "Margem de Lucro")

        # Rotatividade
        tab2 = QWidget()
        tab2_layout = QVBoxLayout(tab2)
        self.table_rotatividade = QTableWidget(0, 4)
        self.table_rotatividade.setHorizontalHeaderLabels([
            "Produto", "Movimentações", "Saídas", "Entradas"
        ])
        tab2_layout.addWidget(self.table_rotatividade)
        tabs.addTab(tab2, "Rotatividade")

        # # Produtos encalhados
        # tab3 = QWidget()
        # tab3_layout = QVBoxLayout(tab3)
        # self.table_encalhados = QTableWidget(0, 5)
        # self.table_encalhados.setHorizontalHeaderLabels([
        #     "Produto", "Qtd", "Data Cadastro", "Dias Parado", "Valor"
        # ])
        # tab3_layout.addWidget(self.table_encalhados)
        # tabs.addTab(tab3, "Produtos Encalhados")

        layout.addWidget(tabs)
        return widget

    def _create_alerts_tab(self):
        """Aba de alertas"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        # Estoque baixo
        group1 = QGroupBox("Produtos com Estoque Baixo")
        group1_layout = QVBoxLayout(group1)
        self.table_estoque_baixo = QTableWidget(0, 4)
        self.table_estoque_baixo.setHorizontalHeaderLabels([
            "Produto", "Qtd", "Mínimo", "Falta"
        ])
        self.table_estoque_baixo.setStyleSheet("QTableWidget { background-color: #224971; }")
        group1_layout.addWidget(self.table_estoque_baixo)
        scroll_layout.addWidget(group1)

        # Próximos de vencer
        group2 = QGroupBox("Produtos Próximos do Vencimento")
        group2_layout = QVBoxLayout(group2)
        self.table_vencimento = QTableWidget(0, 5)
        self.table_vencimento.setHorizontalHeaderLabels([
            "Produto", "Validade", "Qtd", "Dias", "Valor"
        ])
        self.table_vencimento.setStyleSheet("QTableWidget { background-color: #fff3cd;color: #856404; }")
        group2_layout.addWidget(self.table_vencimento)
        scroll_layout.addWidget(group2)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

        return widget

    

    def _create_stat_box(self, title, value):
        """Criar caixa de estatística"""
        widget = QGroupBox(title)
        layout = QVBoxLayout(widget)

        label = QLabel(value)
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        label.setFont(font)
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #0066cc; background-color: #f0f0f0; padding: 10px; border-radius: 5px;")

        layout.addWidget(label)
        widget.label = label  # Guardar referência

        return widget

    def _load_data(self):
        """Carregar todos os dados"""
        try:
            # Estatísticas gerais
            stats = self.service.get_total_statistics()
            self.label_produtos.label.setText(str(stats["total_produtos"]))
            self.label_itens.label.setText(str(stats["total_itens"]))
            self.label_vendas.label.setText(str(stats["total_vendas"]))
            self.label_dias.label.setText(str(stats["dias_com_vendas"]))

            # Estoque
            estoque = self.service.get_stock_metrics()
            self.label_valor_custo.label.setText(f"R$ {estoque['valor_custo']:,.2f}")
            self.label_valor_venda.label.setText(f"R$ {estoque['valor_venda']:,.2f}")
            margem = estoque['valor_venda'] - estoque['valor_custo']
            self.label_margem_total.label.setText(f"R$ {margem:,.2f}")

            # Fiados
            fiados = self.service.get_fiados_summary()
            self.label_fiados.label.setText(f"R$ {fiados['total_open']:,.2f}")

            # Gráficos
            self._draw_sales_chart()
            self._draw_categories_chart()
            self._draw_stock_chart()

            # Tabelas
            self._load_top_products()
            self._load_profit_margins()
            self._load_turnover()
            # self._load_inactive_products()

        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Erro ao carregar dados: {str(e)}")

    def _draw_sales_chart(self):
        """Desenhar gráfico de vendas"""
        try:
            dates, values = self.service.get_sales_chart_data(30)
            
            self.figure_sales.clear()
            ax = self.figure_sales.add_subplot(111)

            if dates and values:
                ax.plot(dates, values, marker='o', linestyle='-', color='#0066cc')
                ax.fill_between(range(len(values)), values, alpha=0.3, color='#0066cc')
                ax.set_xlabel("Data")
                ax.set_ylabel("Faturamento (R$)")
                ax.grid(True, alpha=0.3)
                ax.tick_params(axis='x', rotation=45)

            self.figure_sales.tight_layout()
            self.canvas_sales.draw()
        except Exception as e:
            print(f"Erro ao desenhar gráfico de vendas: {e}")

    def _draw_categories_chart(self):
        """Desenhar gráfico de categorias"""
        try:
            categorias = self.service.get_category_performance()

            self.figure_categories.clear()
            ax = self.figure_categories.add_subplot(111)

            if categorias:
                names = [cat["categoria"] for cat in categorias[:10]]
                values = [cat["faturamento"] for cat in categorias[:10]]

                bars = ax.bar(names, values, color='#28a745')
                ax.set_ylabel("Faturamento (R$)")
                ax.set_title("Top Categorias por Faturamento")
                ax.tick_params(axis='x', rotation=45)

                # Adicionar valores nas barras
                for bar in bars:
                    height = bar.get_height()
                    ax.text(bar.get_x() + bar.get_width()/2., height,
                           f'R${height:,.0f}',
                           ha='center', va='bottom', fontsize=8)

            self.figure_categories.tight_layout()
            self.canvas_categories.draw()
        except Exception as e:
            print(f"Erro ao desenhar gráfico de categorias: {e}")

    def _draw_stock_chart(self):
        """Desenhar gráfico de estoque"""
        try:
            categorias = self.service.get_category_performance()

            self.figure_stock.clear()
            ax = self.figure_stock.add_subplot(111)

            if categorias:
                names = [cat["categoria"] for cat in categorias[:10]]
                values = [cat["produtos"] for cat in categorias[:10]]

                colors = ['#0066cc', '#28a745', '#ff9800', '#e74c3c', '#9b59b6',
                         '#1abc9c', '#f39c12', '#3498db', '#e91e63', '#795548']
                
                wedges, texts, autotexts = ax.pie(values, labels=names, autopct='%1.1f%%',
                                                    colors=colors[:len(names)], startangle=90)
                
                for autotext in autotexts:
                    autotext.set_color('white')
                    autotext.set_fontsize(8)
                    autotext.set_weight('bold')

            self.figure_stock.tight_layout()
            self.canvas_stock.draw()
        except Exception as e:
            print(f"Erro ao desenhar gráfico de estoque: {e}")

    def _load_top_products(self):
        """Carregar tabela de top produtos"""
        try:
            produtos = self.service.get_top_products_data(5)
            self.table_top_produtos.setRowCount(0)

            for produto in produtos:
                row = self.table_top_produtos.rowCount()
                self.table_top_produtos.insertRow(row)

                self.table_top_produtos.setItem(row, 0, QTableWidgetItem(produto["nome"]))
                self.table_top_produtos.setItem(row, 1, QTableWidgetItem(str(produto["quantidade"])))
                self.table_top_produtos.setItem(row, 2, QTableWidgetItem(f"R$ {produto['faturamento']:,.2f}"))
                self.table_top_produtos.setItem(row, 3, QTableWidgetItem(f"R$ {produto['lucro']:,.2f}"))

                if produto["quantidade"] > 0:
                    margem = (produto["lucro"] / produto["faturamento"] * 100) if produto["faturamento"] > 0 else 0
                    self.table_top_produtos.setItem(row, 4, QTableWidgetItem(f"{margem:.1f}%"))
        except Exception as e:
            print(f"Erro ao carregar top produtos: {e}")

    def _load_profit_margins(self):
        """Carregar tabela de margens de lucro"""
        try:
            margens = self.service.get_profit_margins()[:10]
            self.table_margens.setRowCount(0)

            for margem in margens:
                row = self.table_margens.rowCount()
                self.table_margens.insertRow(row)

                self.table_margens.setItem(row, 0, QTableWidgetItem(margem["nome"]))
                self.table_margens.setItem(row, 1, QTableWidgetItem(f"R$ {margem['custo']:.2f}"))
                self.table_margens.setItem(row, 2, QTableWidgetItem(f"R$ {margem['venda']:.2f}"))
                self.table_margens.setItem(row, 3, QTableWidgetItem(f"{margem['margem']:.1f}%"))
                self.table_margens.setItem(row, 4, QTableWidgetItem(f"R$ {margem['lucro_total']:,.2f}"))
        except Exception as e:
            print(f"Erro ao carregar margens: {e}")

    def _load_turnover(self):
        """Carregar tabela de rotatividade"""
        try:
            rotatividade = self.service.get_turnover_analysis(30)[:10]
            self.table_rotatividade.setRowCount(0)

            for item in rotatividade:
                row = self.table_rotatividade.rowCount()
                self.table_rotatividade.insertRow(row)

                self.table_rotatividade.setItem(row, 0, QTableWidgetItem(item["nome"]))
                self.table_rotatividade.setItem(row, 1, QTableWidgetItem(str(item["movimentacoes"])))
                self.table_rotatividade.setItem(row, 2, QTableWidgetItem(str(item["saidas"])))
                self.table_rotatividade.setItem(row, 3, QTableWidgetItem(str(item["entradas"])))
        except Exception as e:
            print(f"Erro ao carregar rotatividade: {e}")

    # def _load_inactive_products(self):
    #     """Carregar tabela de produtos encalhados"""
    #     try:
    #         encalhados = self.service.get_inactive_products(60)[:10]
    #         self.table_encalhados.setRowCount(0)

    #         for item in encalhados:
    #             row = self.table_encalhados.rowCount()
    #             self.table_encalhados.insertRow(row)

    #             self.table_encalhados.setItem(row, 0, QTableWidgetItem(item["nome"]))
    #             self.table_encalhados.setItem(row, 1, QTableWidgetItem(str(item["quantidade"])))
    #             self.table_encalhados.setItem(row, 2, QTableWidgetItem(str(item["data_cadastro"])))
    #             self.table_encalhados.setItem(row, 3, QTableWidgetItem(str(item["dias_parado"])))
    #             self.table_encalhados.setItem(row, 4, QTableWidgetItem(f"R$ {item['valor']:,.2f}"))

    #             # Destacar se > 60 dias parado
    #             if item["dias_parado"] > 60:
    #                 for col in range(5):
    #                     item_widget = self.table_encalhados.item(row, col)
    #                     if item_widget:
    #                         item_widget.setBackground(QColor("#7d765e"))
    #     except Exception as e:
    #         print(f"Erro ao carregar encalhados: {e}")
