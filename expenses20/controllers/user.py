"""
Работа с аккаунтами
"""

from db import select_db, insert_db
from const import STUB_RESULT


class User():
    """
    Работа с аккаунтами
    """
    def create_user(self, name) -> dict:
        """
        Создание нового пользователя
        :param name: имя
        :return: идентификатор
        """
        try:
            res = insert_db('''INSERT INTO User (Name) VALUES(?)''', [name])
            return res
        except Exception as e:
            return {'Result': str(e)}

    def get_all_users(self) -> [dict]:
        """
        Получить всех пользователей
        """
        try:
            users_rows = select_db('''SELECT * FROM User''')
            if users_rows:
                return [{user['Id']: user['Name']} for user in users_rows]
            return STUB_RESULT
        except Exception as e:
            return {'Result': str(e)}

    def get_user_id(self, name) -> int:
        """
        Получить идентификатор пользователя по имени
        :param name: login
        :return: id
        """
        try:
            user = select_db('''SELECT Id FROM User WHERE Name = ?''', [name], True)
            if user:
                return user['Id']
            return None
        except Exception as e:
            return None
