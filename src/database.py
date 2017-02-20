import sqlite3, os

class DB():
    """Класс для работы с базой данных sqllite"""

    CONNECTION_STRING = 'reg_time.db'    

    def __init__(self, connector):
        """Подключает локальную базу данных. Если база не найдена, выдает ошибку"""       
        if os.path.exists(self.CONNECTION_STRING):
            raise 'База данных не найдена'   

        try:
            self.connector = sqlite3.connect(self.CONNECTION_STRING)
        except Exception(e):
            raise 'Попытка подключения к базе данных завершилась неудачно по причине: '+str(e)

    def __execute__(self, command, param = []):
        """Выполняет переданную команду sql с параметрами или без"""
        c = self.connector.cursor()
        result = c.execute(command, param)
        return result

    def __del__(self):
        self.connector.close()