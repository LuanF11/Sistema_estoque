import sys
from PySide6.QtWidgets import QApplication
from database.connection import initialize_database
from ui.windows.main_window import MainWindow

def main():
    # Inicializa o banco de dados
    try:
        initialize_database()
    except Exception as e:
        print(f"Erro ao inicializar o banco de dados: {e}")
        sys.exit(1)

    # Cria a aplicação Qt
    app = QApplication(sys.argv)

    # Cria e exibe a janela principal
    window = MainWindow()
    window.show()

    # Executa o loop principal da aplicação
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
