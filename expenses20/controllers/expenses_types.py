"""
Работа с типами расходов
"""

from db import select_db, insert_db
from const import STUB_RESULT


class ExpensesTypes():
    """
    Записи с типами расходов
    """
    def create_type(self, name) -> dict:
        """
        Создание нового типа расходов
        :param name: название типа
        :return: идентификатор
        """
        try:
            res = insert_db('''INSERT INTO ExpensesTypes (Name) VALUES(?)''', [name])
            return res
        except Exception as e:
            return {'Result': str(e)}

    def get_all_types(self) -> [dict]:
        """
        Получить все типы расходов
        """
        try:
            types_rows = select_db('''SELECT * FROM ExpensesTypes''')
            if types_rows:
                return [{rec['Id']: rec['Name']} for rec in types_rows]
            return STUB_RESULT
        except Exception as e:
            return {'Result': str(e)}
