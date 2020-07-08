import math
import calendar
import pytz
from datetime import date, datetime, timedelta

from django.conf import settings


HTML_DATE_FORMAT = '%Y-%m-%d'
PRETTY_DATE_FORMAT = '%d.%m.%Y'


def now() -> datetime:
    timezone = pytz.timezone(settings.TIME_ZONE)

    return datetime.now(timezone)


def today() -> date:
    return now().date()


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
    quarter_start_ = quarter_start(dt)
    return quarter_start_.replace(month=quarter_start_.month+3) - timedelta(days=1)


def html_date_format(dt: date) -> str:
    return dt.strftime(HTML_DATE_FORMAT)


def date_from_html_format(dt: str) -> date:
    return datetime.strptime(dt, HTML_DATE_FORMAT).date()


def date_pretty_format(dt: date) -> str:
    return dt.strftime(PRETTY_DATE_FORMAT)
