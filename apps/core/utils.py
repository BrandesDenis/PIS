import math
import calendar
from typing import Iterable, Set
from datetime import date, datetime, timedelta

from django.http import QueryDict


HTML_DATE_FORMAT = '%Y-%m-%d'
PRETTY_DATE_FORMAT = '%d.%m.%Y'


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


def html_date_format(dt: date) -> str:
    return dt.strftime(HTML_DATE_FORMAT)


def date_from_html_format(dt: str) -> date:
    return datetime.strptime(dt, HTML_DATE_FORMAT).date()


def date_pretty_format(dt: date) -> str:
    return dt.strftime(PRETTY_DATE_FORMAT)
