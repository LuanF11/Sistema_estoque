from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLineEdit, QListWidget,
    QMessageBox, QLabel
)
from controllers.tag_controller import TagController


class TagWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.controller = TagController()
        self._build_ui()
        self.load_tags()

    def _build_ui(self):
        layout = QVBoxLayout(self)

        # Título
        layout.addWidget(QLabel("Gerenciamento de Tags"))

        # Barra superior (criação)
        top_bar = QHBoxLayout()
        self.tag_input = QLineEdit()
        self.tag_input.setPlaceholderText("Nome da nova tag")

        btn_add = QPushButton("Adicionar")
        btn_add.clicked.connect(self.add_tag)

        top_bar.addWidget(self.tag_input)
        top_bar.addWidget(btn_add)

        # Lista de tags
        self.list_widget = QListWidget()

        # Botão remover
        btn_remove = QPushButton("Remover Tag Selecionada")
        btn_remove.clicked.connect(self.remove_tag)

        layout.addLayout(top_bar)
        layout.addWidget(self.list_widget)
        layout.addWidget(btn_remove)

    def load_tags(self):
        self.list_widget.clear()
        tags = self.controller.list_tags()

        for tag in tags:
            self.list_widget.addItem(f"{tag['id']} - {tag['nome']}")

    def add_tag(self):
        nome = self.tag_input.text().strip()

        result = self.controller.create_tag(nome)
        if result.get("success"):
            self.tag_input.clear()
            self.load_tags()
        else:
            QMessageBox.warning(self, "Erro", result.get("error", "Erro ao criar tag"))

    def remove_tag(self):
        item = self.list_widget.currentItem()
        if not item:
            QMessageBox.warning(self, "Atenção", "Selecione uma tag para remover")
            return

        tag_id = int(item.text().split(" - ")[0])

        confirm = QMessageBox.question(
            self,
            "Confirmação",
            "Tem certeza que deseja remover esta tag?\nProdutos associados perderão essa tag.",
        )

        if confirm == QMessageBox.Yes:
            result = self.controller.delete_tag(tag_id)
            if result.get("success"):
                self.load_tags()
            else:
                QMessageBox.warning(self, "Erro", result.get("error", "Erro ao remover tag"))
