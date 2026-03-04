import sqlite3
from pathlib import Path
import sys

# Caminho para o arquivo do banco de dados SQLite
# Usa a pasta do usuário para persistir dados mesmo quando executado como .exe
def get_db_path():
    # Se rodando como executável PyInstaller, usar pasta na home do usuário
    if getattr(sys, 'frozen', False):
        # Executável PyInstaller - salva em C:\Users\{usuario}\.estoque\estoque.db
        app_data = Path.home() / '.estoque'
        app_data.mkdir(exist_ok=True)
        return app_data / 'estoque.db'
    else:
        # Rodando como script Python normal
        return Path(__file__).parent / 'estoque.db'

DB_PATH = get_db_path()

def get_connection():
    # Cria e retorna uma conexão com o banco de dados SQLite
    # Define o row_factory para sqlite3.Row para acessar colunas por nome
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except sqlite3.Error as e:
        raise Exception(f"Erro ao conectar ao banco de dados: {e}")

def initialize_database():
    # Inicializa o banco de dados executando o script SQL do schema
    try:
        conn = get_connection()
        cursor = conn.cursor()

        # Caminho para o arquivo schema.sql
        Schema_path = Path(__file__).parent / "schema.sql"
        # Lé e executa o script SQL para criar as tabelas
        with open(Schema_path, "r", encoding="utf-8") as f: cursor.executescript(f.read())

        # Migração: Adicionar coluna observacao em fiados se não existir(Estava dando erro lembrar de apagar depois)
        try:
            cursor.execute("ALTER TABLE fiados ADD COLUMN observacao TEXT")
        except sqlite3.OperationalError:
            # Coluna já existe, ignorar
            pass

        # Confirma as mudanças e fecha a conexão
        conn.commit()
        conn.close()
    except FileNotFoundError:
        raise Exception("Arquivo schema.sql não encontrado.")
    except sqlite3.Error as e:
        raise Exception(f"Erro ao inicializar o banco de dados: {e}")
    except Exception as e:
        raise Exception(f"Erro inesperado durante a inicialização: {e}")