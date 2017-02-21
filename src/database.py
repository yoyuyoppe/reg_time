import sqlite3, os

class DB():
    """Класс для работы с базой данных sqllite"""

    CONNECTION_STRING = 'reg_time.db'
    CONNECTOR = None    

    def __init__(self):
        """Подключает локальную базу данных. Если база не найдена, выдает ошибку""" 
        if not os.path.exists(self.CONNECTION_STRING):
            raise 'База данных не найдена'   

        self.CONNECTOR = sqlite3.connect(self.CONNECTION_STRING)

    def __execute__(self, command, param = []):
        """Выполняет переданную команду sql с параметрами или без"""
        c = self.CONNECTOR.cursor()
        result = c.execute(command, param)
        return result

    def __del__(self):
        self.CONNECTOR.close()
        print('finally class DB')

"""try:
    _db = DB()
except Exception(e):
    print('ERROR: %s', e)    

for row in (_db.__execute__('select id, name from users where name = ? and password = ?', ["Администратор", "pkjqjlvby"])):
    print(row[0])

c = _db.__execute__('select * from users where name = ? and password = ?', ["Администратор", "pkjqjlvby"])
print(c.fetchall())

_db = None"""    