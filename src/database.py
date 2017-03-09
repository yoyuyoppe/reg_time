import sqlite3, os

class DB():
    """Класс для работы с базой данных sqllite"""

    CONNECTION_STRING = 'reg_time.db'    

    def __init__(self):
        """Подключает локальную базу данных. Если база не найдена, выдает ошибку""" 
        if not os.path.exists(DB.CONNECTION_STRING):
            raise 'File database not found'   

        self.connector = sqlite3.connect(DB.CONNECTION_STRING)

    def __execute__(self, command, param = []):
        """
        Выполняет переданную команду sql с параметрами или без
        В результате возвращает список найденных строк
        """
        c = self.connector.cursor()
        result = c.execute(command, param)
        return result.fetchall()

    def __del__(self):
        self.connector.close()
 