from django import forms

from apps.finance.models import (Budget, BudgetRow, DayReport, DayReportRow,
                                 PeriodicReport)


class ReportForm(forms.ModelForm):
    class Meta:
        model = DayReport
        exclude = ["total"]


class ReportRowForm(forms.ModelForm):
    class Meta:
        model = DayReportRow
        fields = ["fin_object", "description", "total"]


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        exclude = ["total_income", "total_outcome"]


class BudgetRowForm(forms.ModelForm):
    class Meta:
        model = BudgetRow
        fields = ["fin_object", "total"]


class PeriodicReportForm(forms.ModelForm):
    class Meta:
        model = PeriodicReport
        fields = '__all__'


class NewPeriodicReportForm(forms.Form):
    date = forms.DateField(label='Дата')
    report_type = forms.ChoiceField(choices=PeriodicReport.ReportTypes.choises,
                                    label='Тип')
