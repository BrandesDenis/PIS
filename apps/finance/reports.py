from typing import Dict
from datetime import date
from decimal import Decimal

from apps.core.sql import Query


def report_data(start_date: date, end_date: date) -> Dict:
    query_text = '''
        SELECT
            finance_financeobject.title,
            finance_financeobject.is_positive,
            sum(budgets_total) as budgets,
            sum(reports_total) as reports
        FROM
        (SELECT
            fin_object_id,
            0 as budgets_total,
            total as reports_total
        FROM
            finance_dayreportrow
        WHERE
            date BETWEEN %(start_date)s
                AND %(end_date)s
        UNION ALL
        SELECT
            fin_object_id,
            total,
            0
        FROM
            finance_budgetrow
        WHERE
            date BETWEEN %(start_date)s
                AND %(end_date)s
            ) as rows
        INNER JOIN finance_financeobject
            ON rows.fin_object_id = finance_financeobject.id
        GROUP BY
            finance_financeobject.title,
            finance_financeobject.is_positive
        '''

    params = {
        'start_date': start_date,
        'end_date': end_date,
    }
    data = Query(query_text).execute(params)

    incomes_rows = []
    expenses_rows = []

    incomes_total_reports = Decimal('0.0')
    incomes_total_budgets = Decimal('0.0')

    expenses_total_reports = Decimal('0.0')
    expenses_total_budgets = Decimal('0.0')

    for row in data:

        row['excess'] = row['reports'] > row['budgets']

        if row['is_positive']:
            incomes_rows.append(row)
            incomes_total_reports += row['reports']
            incomes_total_budgets += row['budgets']
        else:
            expenses_rows.append(row)
            expenses_total_reports += row['reports']
            expenses_total_budgets += row['budgets']

    total_reports = incomes_total_reports - expenses_total_reports
    total_budgets = incomes_total_budgets - expenses_total_budgets

    return {
        'incomes_rows': incomes_rows,
        'incomes_total_reports': incomes_total_reports,
        'incomes_total_budgets': incomes_total_budgets,

        'expenses_rows': expenses_rows,
        'expenses_total_reports': expenses_total_reports,
        'expenses_total_budgets': expenses_total_budgets,

        'total_reports': total_reports,
        'total_budgets': total_budgets,
    }
