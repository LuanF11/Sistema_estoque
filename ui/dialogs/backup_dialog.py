from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, 
    QMessageBox, QFileDialog, QTabWidget, QWidget, QTextEdit
)
from PySide6.QtCore import Qt
from pathlib import Path
from services.backup_service import BackupService


class BackupDialog(QDialog):
    """Diálogo para exportar e importar banco de dados"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Backup e Restauração do Banco de Dados")
        self.setMinimumWidth(500)
        self.setMinimumHeight(300)
        
        self._create_ui()

    def _create_ui(self):
        """Cria a interface do usuário"""
        main_layout = QVBoxLayout()
        
        # Cria abas para Exportar e Importar
        tabs = QTabWidget()
        
        # Aba de Exportação
        export_widget = self._create_export_tab()
        tabs.addTab(export_widget, "Exportar Backup")
        
        # Aba de Importação
        import_widget = self._create_import_tab()
        tabs.addTab(import_widget, "Restaurar Backup")
        
        main_layout.addWidget(tabs)
        self.setLayout(main_layout)

    def _create_export_tab(self) -> QWidget:
        """Cria a aba de exportação"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Descrição
        description = QLabel(
            "Exportar seu banco de dados para um local seguro.\n\n"
            "O arquivo será salvo com um timestamp para controle de versões."
        )
        description.setWordWrap(True)
        layout.addWidget(description)
        
        layout.addStretch()
        
        # Botão de exportar
        btn_export = QPushButton("Escolher Pasta e Exportar")
        btn_export.clicked.connect(self._export_database)
        layout.addWidget(btn_export)
        
        widget.setLayout(layout)
        return widget

    def _create_import_tab(self) -> QWidget:
        """Cria a aba de importação"""
        widget = QWidget()
        layout = QVBoxLayout()
        
        # Descrição
        description = QLabel(
            "Restaurar banco de dados de um backup anterior.\n\n"
            "⚠️ ATENÇÃO: Isto irá substituir o banco de dados atual.\n"
            "Um backup de segurança será criado antes da restauração."
        )
        description.setWordWrap(True)
        description.setStyleSheet("color: #d9534f;")
        layout.addWidget(description)
        
        layout.addStretch()
        
        # Botão de importar
        btn_import = QPushButton("Escolher Arquivo e Restaurar")
        btn_import.clicked.connect(self._import_database)
        layout.addWidget(btn_import)
        
        widget.setLayout(layout)
        return widget

    def _export_database(self):
        """Exporta o banco de dados"""
        try:
            # Abre diálogo para escolher pasta
            folder = QFileDialog.getExistingDirectory(
                self,
                "Escolher pasta para exportar backup",
                str(Path.home()),
                options=QFileDialog.ShowDirsOnly
            )
            
            if not folder:
                return
            
            # Exporta o banco de dados
            exported_file = BackupService.export_database(Path(folder))
            
            QMessageBox.information(
                self,
                "Sucesso",
                f"Banco de dados exportado com sucesso!\n\n"
                f"Arquivo: {exported_file.name}\n"
                f"Local: {folder}"
            )
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro na Exportação",
                f"Erro ao exportar banco de dados:\n\n{str(e)}"
            )

    def _import_database(self):
        """Importa o banco de dados"""
        try:
            # Confirma a ação
            reply = QMessageBox.warning(
                self,
                "Confirmar Restauração",
                "Tem certeza que deseja restaurar o banco de dados?\n\n"
                "Um backup de segurança será criado antes.\n"
                "Este processo substitui o banco de dados atual.",
                QMessageBox.Ok | QMessageBox.Cancel
            )
            
            if reply == QMessageBox.Cancel:
                return
            
            # Abre diálogo para escolher arquivo
            file, _ = QFileDialog.getOpenFileName(
                self,
                "Escolher arquivo de backup",
                str(Path.home()),
                "Banco de Dados (*.db);;Todos os Arquivos (*.*)"
            )
            
            if not file:
                return
            
            # Importa o banco de dados
            BackupService.import_database(Path(file))
            
            QMessageBox.information(
                self,
                "Sucesso",
                "Banco de dados restaurado com sucesso!\n\n"
                "A aplicação será reiniciada para recarregar os dados."
            )
            
            # Sinaliza para a aplicação reiniciar
            self.accept()
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Erro na Restauração",
                f"Erro ao restaurar banco de dados:\n\n{str(e)}"
            )
