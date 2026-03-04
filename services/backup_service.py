import shutil
from pathlib import Path
from datetime import datetime
from database.connection import DB_PATH, get_connection
import sqlite3


class BackupService:
    """Serviço para exportar e importar banco de dados"""

    @staticmethod
    def export_database(export_folder: Path) -> Path:
        """
        Exporta o banco de dados para uma pasta com timestamp
        
        Args:
            export_folder: Caminho da pasta onde exportar
            
        Returns:
            Path: Caminho do arquivo exportado
            
        Raises:
            Exception: Se houver erro na exportação
        """
        try:
            # Cria a pasta se não existir
            export_folder = Path(export_folder)
            export_folder.mkdir(parents=True, exist_ok=True)
            
            # Cria nome do arquivo com timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            export_file = export_folder / f"estoque_backup_{timestamp}.db"
            
            # Verifica se o banco de dados existe
            if not DB_PATH.exists():
                raise FileNotFoundError(f"Banco de dados não encontrado em {DB_PATH}")
            
            # Copia o arquivo do banco de dados
            shutil.copy2(DB_PATH, export_file)
            
            return export_file
            
        except Exception as e:
            raise Exception(f"Erro ao exportar banco de dados: {e}")

    @staticmethod
    def import_database(import_file: Path) -> None:
        """
        Importa um banco de dados de backup
        
        Args:
            import_file: Caminho do arquivo de backup para importar
            
        Raises:
            Exception: Se houver erro na importação
        """
        try:
            import_file = Path(import_file)
            
            # Verifica se o arquivo existe
            if not import_file.exists():
                raise FileNotFoundError(f"Arquivo não encontrado: {import_file}")
            
            # Verifica se é um arquivo válido de banco de dados SQLite
            try:
                conn = sqlite3.connect(import_file)
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
                conn.close()
            except sqlite3.DatabaseError:
                raise ValueError("Arquivo selecionado não é um banco de dados válido")
            
            # Cria backup do banco atual antes de sobrescrever
            current_backup = BackupService._create_safety_backup(DB_PATH)
            
            try:
                # Copia o arquivo de importação para o local do banco de dados
                shutil.copy2(import_file, DB_PATH)
                
            except Exception as e:
                # Se falhar, restaura o backup de segurança
                if current_backup.exists():
                    shutil.copy2(current_backup, DB_PATH)
                raise Exception(f"Erro ao restaurar banco de dados: {e}")
            
        except Exception as e:
            raise Exception(f"Erro ao importar banco de dados: {e}")

    @staticmethod
    def _create_safety_backup(db_file: Path) -> Path:
        """
        Cria backup de segurança do banco de dados atual
        
        Args:
            db_file: Caminho do arquivo do banco de dados
            
        Returns:
            Path: Caminho do arquivo de backup
        """
        try:
            backup_file = db_file.parent / f".{db_file.stem}_safety_backup.db"
            if db_file.exists():
                shutil.copy2(db_file, backup_file)
            return backup_file
        except Exception as e:
            raise Exception(f"Erro ao criar backup de segurança: {e}")

    @staticmethod
    def verify_database_integrity(db_file: Path) -> bool:
        """
        Verifica a integridade do arquivo do banco de dados
        
        Args:
            db_file: Caminho do arquivo para verificar
            
        Returns:
            bool: True se o banco está íntegro, False caso contrário
        """
        try:
            if not db_file.exists():
                return False
                
            conn = sqlite3.connect(db_file)
            cursor = conn.cursor()
            cursor.execute("PRAGMA integrity_check;")
            result = cursor.fetchone()
            conn.close()
            
            return result[0] == "ok"
        except Exception:
            return False
