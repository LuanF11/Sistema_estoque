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

        # Migração: adicionar coluna produto_nome para armazenar nome quando produto não estiver cadastrado
        try:
            cursor.execute("ALTER TABLE fiados ADD COLUMN produto_nome TEXT")
        except sqlite3.OperationalError:
            pass

        # Migração: permitir null em produto_id caso tabela antiga tenha NOT NULL
        # SQLite não remove NOT NULL via ALTER, portanto recriamos a tabela se necessário
        info = cursor.execute("PRAGMA table_info(fiados)").fetchall()
        for col in info:
            # col format: (cid, name, type, notnull, dflt_value, pk)
            if col[1] == 'produto_id' and col[3] == 1:
                # precisamos recriar tabela com produto_id aceitando NULL
                cursor.execute("ALTER TABLE fiados RENAME TO fiados_old")
                cursor.executescript("""
                CREATE TABLE fiados (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    cliente_id INTEGER NOT NULL,
                    produto_id INTEGER,
                    produto_nome TEXT,
                    quantidade INTEGER NOT NULL,
                    valor_unitario REAL NOT NULL,
                    valor_total REAL NOT NULL,
                    valor_pendente REAL NOT NULL,
                    observacao TEXT,
                    data_fiado TEXT NOT NULL DEFAULT (DATE('now')),
                    data_vencimento TEXT,
                    FOREIGN KEY (cliente_id) REFERENCES clientes (id),
                    FOREIGN KEY (produto_id) REFERENCES produtos (id)
                );
                """
                )
                cursor.execute(
                    "INSERT INTO fiados (id, cliente_id, produto_id, produto_nome, quantidade, valor_unitario,\
                     valor_total, valor_pendente, observacao, data_fiado, data_vencimento)\
                     SELECT id, cliente_id, produto_id, produto_nome, quantidade, valor_unitario,\
                     valor_total, valor_pendente, observacao, data_fiado, data_vencimento\
                     FROM fiados_old"
                )
                cursor.execute("DROP TABLE fiados_old")
                break

        # Confirma as mudanças e fecha a conexão
        conn.commit()
        conn.close()
    except FileNotFoundError:
        raise Exception("Arquivo schema.sql não encontrado.")
    except sqlite3.Error as e:
        raise Exception(f"Erro ao inicializar o banco de dados: {e}")
    except Exception as e:
        raise Exception(f"Erro inesperado durante a inicialização: {e}")