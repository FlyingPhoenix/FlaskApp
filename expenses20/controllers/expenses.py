"""
Записи с расходами
"""

from db import select_db, insert_db
from const import STUB_RESULT


class Expenses():
    """
    Записи с расходами
    """
    def create_record(self, params: dict) -> dict:
        """
        Создание нового пользователя
        :param name: имя
        :return: идентификатор новой записи
        """
        try:
            params_list = [params.get('user'), params.get('type'), params.get('sum'), params.get('description'),
                           params.get('r_date')]
            res = insert_db('''INSERT INTO Expenses (User, Type, Sum, Description, RDate) VALUES(?, ?, ?, ?, ?)''',
                            params_list)
            return res
        except Exception as e:
            return {'Result': str(e)}
