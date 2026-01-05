from database.connection import get_connection

class BaseRepository:

    '''
    Classe base para repositórios de banco de dados, 
    fornecendo métodos comuns para executar consultas SQL.
    '''

    # Método para executar uma consulta SQL sem retorno
    def execute(self, query: str, params: tuple = ()):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        conn.commit()
        cursor.close()

    # Método para executar uma consulta SQL que retorna um único registro
    def fetchone(self, query: str, params: tuple = ()):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        result = cursor.fetchone()
        cursor.close()
        return result
    
    # Método para executar uma consulta SQL que retorna múltiplos registros
    def fetchall(self, query: str, params: tuple = ()):
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()
        return results
            

        
        
