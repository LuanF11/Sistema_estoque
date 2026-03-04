from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QTableWidget, QTableWidgetItem, QScrollArea,
    QGroupBox, QTabWidget, QMessageBox, QPushButton
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QColor
from services.analytics_service import AnalyticsService
from controllers.stock_controller import StockController
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class AnalyticsWindow(QWidget):
    """Dashboard com análises avançadas de dados"""

    def __init__(self):
        super().__init__()
        self.service = AnalyticsService()
        # controller usado para operações que afetam dados
        self.controller = StockController()
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
        
        # Aba 5: Análise de Prejuízos
        tabs.addTab(self._create_losses_tab(), "Análise de Prejuízos")
        # Aba 6: Análise de Fiados
        tabs.addTab(self._create_fiados_tab(), "Análise de Fiados")

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
        self.label_prejuizos = self._create_stat_box("Prejuízos (R$)", "R$ 0,00")

        stats_layout.addWidget(self.label_produtos)
        stats_layout.addWidget(self.label_itens)
        stats_layout.addWidget(self.label_vendas)
        stats_layout.addWidget(self.label_dias)
        stats_layout.addWidget(self.label_fiados)
        stats_layout.addWidget(self.label_prejuizos)

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

        # Prejuizos por motivo
        group_p = QGroupBox("Prejuízos por Motivo")
        group_p_layout = QVBoxLayout(group_p)
        self.table_prejuizos = QTableWidget(0, 3)
        self.table_prejuizos.setHorizontalHeaderLabels(["Motivo", "Qtd", "Valor Total (R$)"])
        group_p_layout.addWidget(self.table_prejuizos)
        layout.addWidget(group_p)

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

    def _create_losses_tab(self):
        """Aba de análise de prejuízos"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Estatísticas de prejuízos
        stats_layout = QHBoxLayout()
        self.label_total_losses = self._create_stat_box("Total de Prejuízos", "R$ 0,00")
        self.label_losses_count = self._create_stat_box("Quantidade de Registros", "0")
        stats_layout.addWidget(self.label_total_losses)
        stats_layout.addWidget(self.label_losses_count)
        layout.addLayout(stats_layout)

        # Resumo de prejuízos por motivo
        group = QGroupBox("Prejuízos por Motivo")
        group_layout = QVBoxLayout(group)

        self.table_losses_by_motivo = QTableWidget(0, 3)
        self.table_losses_by_motivo.setHorizontalHeaderLabels([
            "Motivo", "Qtd", "Valor Total (R$)"
        ])
        group_layout.addWidget(self.table_losses_by_motivo)
        layout.addWidget(group)

        # Lista detalhada de prejuízos
        group_detail = QGroupBox("Detalhamento de Todos os Prejuízos")
        group_detail_layout = QVBoxLayout(group_detail)

        self.table_losses_detail = QTableWidget(0, 8)
        self.table_losses_detail.setHorizontalHeaderLabels([
            "ID", "Produto", "Qtd", "Valor Unit.", "Valor Total", "Motivo", "Observação", "Data"
        ])
        self.table_losses_detail.setColumnWidth(6, 200)
        group_detail_layout.addWidget(self.table_losses_detail)

        # botão de excluir prejuízo selecionado
        btn_layout = QHBoxLayout()
        self.btn_delete_loss = QPushButton("Excluir Prejuízo Selecionado")
        self.btn_delete_loss.clicked.connect(self._on_delete_prejuizo)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_delete_loss)
        group_detail_layout.addLayout(btn_layout)

        layout.addWidget(group_detail)

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

            # Fiados (visão geral)
            fiados = self.service.get_fiados_summary()
            self.label_fiados.label.setText(f"R$ {fiados['total_open']:,.2f}")

            # Prejuizos
            preju = self.service.get_prejuizos_summary()
            self.label_prejuizos.label.setText(f"R$ {preju['total_valor']:,.2f}")

            # Gráficos
            self._draw_sales_chart()
            self._draw_categories_chart()
            self._draw_stock_chart()

            # Tabelas
            self._load_top_products()
            self._load_prejuizos()
            self._load_losses_detail()
            self._load_profit_margins()
            self._load_turnover()
            self._load_fiados_tab()
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

    def _load_prejuizos(self):
        try:
            prej = self.service.get_prejuizos_by_motivo(10)
            self.table_prejuizos.setRowCount(0)
            for item in prej:
                row = self.table_prejuizos.rowCount()
                self.table_prejuizos.insertRow(row)
                self.table_prejuizos.setItem(row, 0, QTableWidgetItem(item['motivo']))
                self.table_prejuizos.setItem(row, 1, QTableWidgetItem(str(item['count'])))
                self.table_prejuizos.setItem(row, 2, QTableWidgetItem(f"R$ {item['total']:,.2f}"))
        except Exception as e:
            print(f"Erro ao carregar prejuizos: {e}")

    def _load_losses_detail(self):
        """Carregar tabelas detalhadas de prejuízos"""
        try:
            # Carregar prejuízos por motivo na aba de prejuízos
            prej_motivo = self.service.get_prejuizos_by_motivo(10)
            self.table_losses_by_motivo.setRowCount(0)
            for item in prej_motivo:
                row = self.table_losses_by_motivo.rowCount()
                self.table_losses_by_motivo.insertRow(row)
                self.table_losses_by_motivo.setItem(row, 0, QTableWidgetItem(item['motivo']))
                self.table_losses_by_motivo.setItem(row, 1, QTableWidgetItem(str(item['count'])))
                self.table_losses_by_motivo.setItem(row, 2, QTableWidgetItem(f"R$ {item['total']:,.2f}"))

            # Carregar lista detalhada de prejuízos
            from utils.dates import format_date
            prejuizos = self.service.get_prejuizos_detalhados()
            self.table_losses_detail.setRowCount(0)
            
            total_value = 0
            total_count = 0
            
            for prej in prejuizos:
                row = self.table_losses_detail.rowCount()
                self.table_losses_detail.insertRow(row)
                
                self.table_losses_detail.setItem(row, 0, QTableWidgetItem(str(prej['id'])))
                self.table_losses_detail.setItem(row, 1, QTableWidgetItem(str(prej['produto_nome'])))
                self.table_losses_detail.setItem(row, 2, QTableWidgetItem(str(prej['quantidade'])))
                self.table_losses_detail.setItem(row, 3, QTableWidgetItem(f"R$ {prej['valor_unitario']:,.2f}"))
                self.table_losses_detail.setItem(row, 4, QTableWidgetItem(f"R$ {prej['valor_total']:,.2f}"))
                self.table_losses_detail.setItem(row, 5, QTableWidgetItem(str(prej['motivo'])))
                self.table_losses_detail.setItem(row, 6, QTableWidgetItem(str(prej['observacao'] if prej['observacao'] else "-")))
                self.table_losses_detail.setItem(row, 7, QTableWidgetItem(format_date(str(prej['data_prejuizo']))))
                
                # Acumular os totais
                total_value += prej['valor_total']
                total_count += 1
            
            # Atualizar as caixas de estatística com os totais
            self.label_total_losses.label.setText(f"R$ {total_value:,.2f}")
            self.label_losses_count.label.setText(str(total_count))
        except Exception as e:
            print(f"Erro ao carregar detalhamento de prejuízos: {e}")

    def _create_fiados_tab(self):
        """Aba de análise de fiados"""
        widget = QWidget()
        layout = QVBoxLayout(widget)

        # Estatísticas de fiados
        stats_layout = QHBoxLayout()
        self.label_open_count = self._create_stat_box("Fiados em Aberto", "0")
        self.label_open_value = self._create_stat_box("Valor Aberto (R$)", "R$ 0,00")
        self.label_paid_count = self._create_stat_box("Fiados Pagos", "0")
        self.label_paid_value = self._create_stat_box("Valor Pago (R$)", "R$ 0,00")
        stats_layout.addWidget(self.label_open_count)
        stats_layout.addWidget(self.label_open_value)
        stats_layout.addWidget(self.label_paid_count)
        stats_layout.addWidget(self.label_paid_value)
        layout.addLayout(stats_layout)

        # Tabela detalhada de fiados
        group = QGroupBox("Detalhamento de Fiados")
        group_layout = QVBoxLayout(group)

        self.table_fiados = QTableWidget(0, 8)
        self.table_fiados.setHorizontalHeaderLabels([
            "ID", "Cliente", "Produto", "Qtd", "Valor Total", "Pago", "Data Fiado", "Data Pagamento"
        ])
        self.table_fiados.setColumnWidth(7, 150)
        group_layout.addWidget(self.table_fiados)

        # botão para gerenciar (abre diálogo)
        btn_layout = QHBoxLayout()
        self.btn_manage_fiados2 = QPushButton("Gerenciar Fiados")
        self.btn_manage_fiados2.clicked.connect(self._open_fiado_manager)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_manage_fiados2)
        group_layout.addLayout(btn_layout)

        layout.addWidget(group)
        return widget

    def _load_fiados_tab(self):
        try:
            # estatísticas
            stats = self.service.get_fiados_summary()
            self.label_open_count.label.setText(str(stats['count_open']))
            self.label_open_value.label.setText(f"R$ {stats['total_open']:,.2f}")
            self.label_paid_count.label.setText(str(stats['count_paid']))
            self.label_paid_value.label.setText(f"R$ {stats['total_paid']:,.2f}")

            from utils.dates import format_date
            fiados = self.service.get_fiados_detalhados()
            self.table_fiados.setRowCount(0)
            for f in fiados:
                row = self.table_fiados.rowCount()
                self.table_fiados.insertRow(row)
                self.table_fiados.setItem(row, 0, QTableWidgetItem(str(f['id'])))
                self.table_fiados.setItem(row, 1, QTableWidgetItem(str(f['cliente'])))
                self.table_fiados.setItem(row, 2, QTableWidgetItem(str(f['produto_nome'])))
                self.table_fiados.setItem(row, 3, QTableWidgetItem(str(f['quantidade'])))
                self.table_fiados.setItem(row, 4, QTableWidgetItem(f"R$ {f['valor_total']:,.2f}"))
                self.table_fiados.setItem(row, 5, QTableWidgetItem("Sim" if f['pago'] else "Não"))
                self.table_fiados.setItem(row, 6, QTableWidgetItem(format_date(str(f['data_fiado']))))
                self.table_fiados.setItem(row, 7, QTableWidgetItem(format_date(str(f['data_pagamento'])) if f['data_pagamento'] else "-"))
        except Exception as e:
            print(f"Erro ao carregar aba de fiados: {e}")

    def _on_delete_prejuizo(self):
        """Handler para remover prejuízo selecionado"""
        row = self.table_losses_detail.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Aviso", "Selecione um prejuízo na lista")
            return

        prej_id_item = self.table_losses_detail.item(row, 0)
        if not prej_id_item:
            QMessageBox.warning(self, "Aviso", "ID do prejuízo inválido")
            return

        prej_id = int(prej_id_item.text())
        resp = QMessageBox.question(
            self,
            "Confirmação",
            f"Deseja realmente excluir o prejuízo #{prej_id}? Esta operação irá repor o estoque.",
            QMessageBox.Yes | QMessageBox.No
        )
        if resp != QMessageBox.Yes:
            return

        result = self.controller.delete_prejuizo(prej_id)
        if result.get("success"):
            QMessageBox.information(self, "Sucesso", "Prejuízo excluído e estoque ajustado.")
            self._load_data()
        else:
            QMessageBox.warning(self, "Erro", result.get("error", "Não foi possível excluir o prejuízo"))

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

    def _open_fiado_manager(self):
        """Abre o diálogo de gerenciamento de fiados"""
        from ui.dialogs.fiado_manager import FiadoManagerDialog
        dlg = FiadoManagerDialog(self)
        dlg.exec()

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
    def refresh(self):
        """Recarrega os dados quando a aba fica visível."""
        self._load_data()