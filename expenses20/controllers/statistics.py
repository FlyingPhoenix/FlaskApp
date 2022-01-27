"""
Статистика расходов
"""

import calendar
from datetime import datetime
from db import select_db
from const import STUB_RESULT


class Statistics():
    """
    Статистика расходов
    """
    def month_sum(self, year, month):
        """
        Общая сумма затрат за месяц
        :param year: год
        :param month: месяц
        :return: {'user_name': sum}
        """
        try:
            days = calendar.monthrange(int(year), int(month))
            first_date = datetime.strptime(f"{year}-{month}-01", '%Y-%m-%d')
            last_date = datetime.strptime(f"{year}-{month}-{days[1]}", '%Y-%m-%d')
            result = select_db('''
                SELECT
                    u."Name" AS "User",
                    SUM("Sum") AS "Sum"
                FROM
                    Expenses e
                    INNER JOIN User u ON e."User" = u."Id"
                WHERE
                    e."RDate" BETWEEN ? AND ?
                GROUP BY
                    e."User"
            ''', [first_date, last_date])
            if result:
                return [{rec['User']: rec['Sum']} for rec in result]
            return res
        except Exception as e:
            return {'Result': str(e)}
