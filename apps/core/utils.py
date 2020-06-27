import math
import calendar
from typing import Iterable, Set
from datetime import date, timedelta

from django.http import QueryDict

SQL_DATE_FORMAT = '%Y-%m-%d'


def collect_rows_from_request(request_data: QueryDict,
                              columns: Iterable[str]) -> Iterable[Set]:

    columns_data = []
    for column in columns:
        column_data = request_data.getlist(column)
        columns_data.append(column_data)

    return zip(*columns_data)


def week_start(dt: date) -> date:
    return dt - timedelta(days=dt.weekday())


def week_end(dt: date) -> date:
    return week_start(dt) + timedelta(days=6)


def month_start(dt: date) -> date:
    return dt.replace(day=1)


def month_end(dt: date) -> date:
    return dt.replace(day=calendar.monthrange(dt.year, dt.month)[1])


def quarter_start(dt: date) -> date:
    quarter = math.ceil(dt.month/3)
    return date(dt.year, 3 * quarter - 2, 1)


def quarter_end(dt: date) -> date:
    return quarter_start(dt).replace(month=dt.month+3) - timedelta(days=1)
