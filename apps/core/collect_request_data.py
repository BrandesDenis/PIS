from typing import Iterable, Set, Tuple
from datetime import date

from django.http import QueryDict

from apps.core.dates import today, month_start, month_end, date_from_html_format


def collect_rows(request_data: QueryDict,
                 columns: Iterable[str]) -> Iterable[Set]:

    columns_data = []
    for column in columns:
        column_data = request_data.getlist(column)
        columns_data.append(column_data)

    return zip(*columns_data)


def collect_start_end_dates_reports(request_data: QueryDict) -> Tuple[date]:
    today_date = today()

    start_date_param = request_data.get('start_date')
    if start_date_param:
        start_date = date_from_html_format(start_date_param)
    else:
        start_date = month_start(today_date)

    end_date_param = request_data.get('end_date')
    if end_date_param:
        end_date = date_from_html_format(end_date_param)
    else:
        end_date = month_end(today_date)

    return start_date, end_date
