from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QSpinBox, QPushButton, QDialog,
    QMessageBox, QGroupBox, QDoubleSpinBox, QGridLayout
)
from PySide6.QtCore import Qt, QDateTime
from PySide6.QtGui import QFont, QColor

from controllers.caixa_controller import CaixaController
from utils.dates import format_date


class CaixaDialog(QDialog):
    """Dialog para abertura de caixa."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Abrir Caixa")
        self.setMinimumWidth(300)
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel("Valor de Abertura (R$):"))
        self.spinbox_valor = QDoubleSpinBox()
        self.spinbox_valor.setMinimum(0)
        self.spinbox_valor.setMaximum(999999)
        self.spinbox_valor.setDecimals(2)
        self.spinbox_valor.setValue(0)
        layout.addWidget(self.spinbox_valor)

        buttons_layout = QHBoxLayout()
        btn_ok = QPushButton("Abrir")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        
        buttons_layout.addWidget(btn_ok)
        buttons_layout.addWidget(btn_cancel)
        layout.addLayout(buttons_layout)

    def get_valor(self):
        return self.spinbox_valor.value()


class FecharCaixaDialog(QDialog):
    """Dialog para fechamento de caixa."""

    def __init__(self, valor_abertura: float, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Fechar Caixa")
        self.setMinimumWidth(350)
        self.valor_abertura = valor_abertura
        self._build_ui()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        
        layout.addWidget(QLabel(f"Valor de Abertura: R$ {self.valor_abertura:.2f}"))
        
        layout.addWidget(QLabel("Valor de Fechamento (R$):"))
        self.spinbox_valor = QDoubleSpinBox()
        self.spinbox_valor.setMinimum(0)
        self.spinbox_valor.setMaximum(999999)
        self.spinbox_valor.setDecimals(2)
        self.spinbox_valor.setValue(self.valor_abertura)
        layout.addWidget(self.spinbox_valor)

        buttons_layout = QHBoxLayout()
        btn_ok = QPushButton("Fechar")
        btn_ok.clicked.connect(self.accept)
        btn_cancel = QPushButton("Cancelar")
        btn_cancel.clicked.connect(self.reject)
        
        buttons_layout.addWidget(btn_ok)
        buttons_layout.addWidget(btn_cancel)
        layout.addLayout(buttons_layout)

    def get_valor(self):
        return self.spinbox_valor.value()


class HomeScreen(QWidget):

    def __init__(self):
        super().__init__()
        self.caixa_controller = CaixaController()
        self.caixa_atual = None
        self._build_ui()
        self.atualizar_status_caixa()

    def showEvent(self, event):
        """Atualiza dados quando a tela fica visível."""
        super().showEvent(event)
        self.atualizar_status_caixa()

    def _build_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(30, 30, 30, 30)

        # Título
        titulo = QLabel("Controle de Caixa")
        titulo_font = QFont()
        titulo_font.setPointSize(16)
        titulo_font.setBold(True)
        titulo.setFont(titulo_font)
        layout.addWidget(titulo)

        # Grupo de status
        status_group = QGroupBox("Status do Caixa")
        status_layout = QVBoxLayout()

        # Status visual
        self.status_label = QLabel()
        self.status_label.setFont(QFont("Arial", 12, QFont.Bold))
        status_layout.addWidget(self.status_label)

        # Informações
        self.info_layout = QVBoxLayout()
        status_layout.addLayout(self.info_layout)

        status_group.setLayout(status_layout)
        layout.addWidget(status_group)

        # Botões
        buttons_layout = QHBoxLayout()
        
        self.btn_abrir = QPushButton("Abrir Caixa")
        self.btn_abrir.setMinimumHeight(50)
        self.btn_abrir.setMinimumWidth(150)
        self.btn_abrir.clicked.connect(self.abrir_caixa)
        
        self.btn_fechar = QPushButton("Fechar Caixa")
        self.btn_fechar.setMinimumHeight(50)
        self.btn_fechar.setMinimumWidth(150)
        self.btn_fechar.clicked.connect(self.fechar_caixa)
        self.btn_fechar.setEnabled(False)

        buttons_layout.addWidget(self.btn_abrir)
        buttons_layout.addWidget(self.btn_fechar)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        layout.addStretch()

    def atualizar_status_caixa(self):
        """Atualiza o status do caixa na tela."""
        self.caixa_atual = self.caixa_controller.get_caixa_hoje()
        
        # Limpa layout de informações
        while self.info_layout.count():
            self.info_layout.takeAt(0).widget().deleteLater()

        if self.caixa_atual:
            if self.caixa_atual["status"] == "ABERTO":
                self.status_label.setText("🟢 CAIXA ABERTO")
                self.status_label.setStyleSheet("color: #27ae60; font-weight: bold;")
                self.btn_abrir.setEnabled(False)
                self.btn_fechar.setEnabled(True)
            else:
                self.status_label.setText("🔴 CAIXA FECHADO")
                self.status_label.setStyleSheet("color: #e74c3c; font-weight: bold;")
                self.btn_abrir.setEnabled(False)
                self.btn_fechar.setEnabled(False)

            # Cria cards informativos
            info_grid = QGridLayout()
            info_grid.setSpacing(15)
            
            # Card: Data
            data_label = QLabel("📅 Data")
            data_label.setFont(QFont("Arial", 10, QFont.Bold))
            data_label.setStyleSheet("color: #0d47a1;")
            data_value = QLabel(format_date(self.caixa_atual['data']))
            data_value.setFont(QFont("Arial", 11))
            data_value.setStyleSheet("color: #1565c0;")
            data_card = QVBoxLayout()
            data_card.addWidget(data_label)
            data_card.addWidget(data_value)
            data_widget = QGroupBox()
            data_widget.setLayout(data_card)
            data_widget.setStyleSheet("QGroupBox { background-color: #e8f4f8; padding: 10px; border-radius: 5px; border: 1px solid #b3d9e6; }")
            
            # Card: Valor de Abertura
            abertura_label = QLabel("💰 Valor de Abertura")
            abertura_label.setFont(QFont("Arial", 10, QFont.Bold))
            abertura_label.setStyleSheet("color: #1b5e20;")
            abertura_value = QLabel(f"R$ {self.caixa_atual['valor_abertura']:.2f}")
            abertura_value.setFont(QFont("Arial", 11, QFont.Bold))
            abertura_value.setStyleSheet("color: #2e7d32;")
            abertura_card = QVBoxLayout()
            abertura_card.addWidget(abertura_label)
            abertura_card.addWidget(abertura_value)
            abertura_widget = QGroupBox()
            abertura_widget.setLayout(abertura_card)
            abertura_widget.setStyleSheet("QGroupBox { background-color: #d5f4e6; padding: 10px; border-radius: 5px; border: 1px solid #7dd3c0; }")
            
            # Card: Hora de Abertura
            hora_label = QLabel("🕐 Hora de Abertura")
            hora_label.setFont(QFont("Arial", 10, QFont.Bold))
            hora_label.setStyleSheet("color: #f57f17;")
            hora_value = QLabel(str(self.caixa_atual['data_abertura']))
            hora_value.setFont(QFont("Arial", 11))
            hora_value.setStyleSheet("color: #f9a825;")
            hora_card = QVBoxLayout()
            hora_card.addWidget(hora_label)
            hora_card.addWidget(hora_value)
            hora_widget = QGroupBox()
            hora_widget.setLayout(hora_card)
            hora_widget.setStyleSheet("QGroupBox { background-color: #fff9e6; padding: 10px; border-radius: 5px; border: 1px solid #ffe680; }")
            
            # Adiciona cards na primeira linha
            info_grid.addWidget(data_widget, 0, 0)
            info_grid.addWidget(abertura_widget, 0, 1)
            info_grid.addWidget(hora_widget, 0, 2)
            
            # Se fechado, adiciona informações de fechamento
            if self.caixa_atual["valor_fechamento"]:
                # Card: Valor de Fechamento
                fechamento_label = QLabel("💵 Valor de Fechamento")
                fechamento_label.setFont(QFont("Arial", 10, QFont.Bold))
                fechamento_label.setStyleSheet("color: #880e4f;")
                fechamento_value = QLabel(f"R$ {self.caixa_atual['valor_fechamento']:.2f}")
                fechamento_value.setFont(QFont("Arial", 11, QFont.Bold))
                fechamento_value.setStyleSheet("color: #c2185b;")
                fechamento_card = QVBoxLayout()
                fechamento_card.addWidget(fechamento_label)
                fechamento_card.addWidget(fechamento_value)
                fechamento_widget = QGroupBox()
                fechamento_widget.setLayout(fechamento_card)
                fechamento_widget.setStyleSheet("QGroupBox { background-color: #f0d5e6; padding: 10px; border-radius: 5px; border: 1px solid #d99ec3; }")
                
                # Card: Hora de Fechamento
                hora_fech_label = QLabel("🕕 Hora de Fechamento")
                hora_fech_label.setFont(QFont("Arial", 10, QFont.Bold))
                hora_fech_label.setStyleSheet("color: #f57f17;")
                hora_fech_value = QLabel(str(self.caixa_atual['data_fechamento']))
                hora_fech_value.setFont(QFont("Arial", 11))
                hora_fech_value.setStyleSheet("color: #f9a825;")
                hora_fech_card = QVBoxLayout()
                hora_fech_card.addWidget(hora_fech_label)
                hora_fech_card.addWidget(hora_fech_value)
                hora_fech_widget = QGroupBox()
                hora_fech_widget.setLayout(hora_fech_card)
                hora_fech_widget.setStyleSheet("QGroupBox { background-color: #fff9e6; padding: 10px; border-radius: 5px; border: 1px solid #ffe680; }")
                
                # Card: Diferença
                diferenca = self.caixa_atual["valor_fechamento"] - self.caixa_atual["valor_abertura"]
                cor_diferenca = "#d5f4e6" if diferenca >= 0 else "#f4d5d5"
                cor_borda = "#7dd3c0" if diferenca >= 0 else "#d97d7d"
                cor_texto = "#1b5e20" if diferenca >= 0 else "#b71c1c"
                diferenca_label = QLabel("📊 Diferença")
                diferenca_label.setFont(QFont("Arial", 10, QFont.Bold))
                diferenca_label.setStyleSheet(f"color: {cor_texto};")
                diferenca_value = QLabel(f"R$ {diferenca:.2f}")
                diferenca_value.setFont(QFont("Arial", 11, QFont.Bold))
                diferenca_value.setStyleSheet(f"color: {'#2e7d32' if diferenca >= 0 else '#d32f2f'};")
                diferenca_card = QVBoxLayout()
                diferenca_card.addWidget(diferenca_label)
                diferenca_card.addWidget(diferenca_value)
                diferenca_widget = QGroupBox()
                diferenca_widget.setLayout(diferenca_card)
                diferenca_widget.setStyleSheet(f"QGroupBox {{ background-color: {cor_diferenca}; padding: 10px; border-radius: 5px; border: 1px solid {cor_borda}; }}")
                
                # Adiciona cards na segunda linha
                info_grid.addWidget(fechamento_widget, 1, 0)
                info_grid.addWidget(hora_fech_widget, 1, 1)
                info_grid.addWidget(diferenca_widget, 1, 2)
            
            grid_widget = QWidget()
            grid_widget.setLayout(info_grid)
            self.info_layout.addWidget(grid_widget)
        else:
            self.status_label.setText("⚫ CAIXA NÃO ABERTO")
            self.status_label.setStyleSheet("color: #34495e; font-weight: bold;")
            self.btn_abrir.setEnabled(True)
            self.btn_fechar.setEnabled(False)
            
            info_label = QLabel("Nenhum caixa aberto hoje. Clique em 'Abrir Caixa' para iniciar.")
            info_label.setStyleSheet("background-color: #ecf0f1; color: #2c3e50; padding: 15px; border-radius: 5px; border: 1px solid #bdc3c7;")
            info_label.setFont(QFont("Arial", 11))
            self.info_layout.addWidget(info_label)

    def abrir_caixa(self):
        """Abre um novo caixa."""
        dialog = CaixaDialog(self)
        if dialog.exec() == QDialog.Accepted:
            valor = dialog.get_valor()
            
            result = self.caixa_controller.abrir_caixa(valor)
            
            if result["success"]:
                QMessageBox.information(self, "Sucesso", result["message"])
                self.atualizar_status_caixa()
            else:
                QMessageBox.warning(self, "Erro", result["error"])

    def fechar_caixa(self):
        """Fecha o caixa."""
        if not self.caixa_atual:
            QMessageBox.warning(self, "Erro", "Nenhum caixa aberto")
            return

        dialog = FecharCaixaDialog(self.caixa_atual["valor_abertura"], self)
        if dialog.exec() == QDialog.Accepted:
            valor = dialog.get_valor()
            
            result = self.caixa_controller.fechar_caixa(self.caixa_atual["id"], valor)
            
            if result["success"]:
                msg = f"""{result['message']}

                Abertura: R$ {result['valor_abertura']:.2f}
                Fechamento: R$ {result['valor_fechamento']:.2f}
                Diferença: R$ {result['diferenca']:.2f}"""
                QMessageBox.information(self, "Sucesso", msg)
                self.atualizar_status_caixa()
            else:
                QMessageBox.warning(self, "Erro", result["error"])
