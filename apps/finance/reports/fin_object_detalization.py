from typing import Dict
from datetime import date

from django.db.models import Sum

from apps.finance.models import FinanceObject, DayReportRow


def fin_object_detalization(start_date: date,
                            end_date: date,
                            fin_object: FinanceObject) -> Dict:

    report_rows = DayReportRow.objects.filter(fin_object=fin_object)\
        .filter(date__range=(start_date, end_date))\
        .values('date', 'total', 'document')

    total = report_rows.aggregate(Sum('total')).get('total__sum', 0)

    return {
        'report_rows': report_rows,
        'total': total,
    }
