from django import forms

from apps.finance.models import (Budget, BudgetRow, DayReport, DayReportRow,
                                 PeriodicReport, FinanceObject)


class FinanceRowForm(forms.ModelForm):
    fin_object = forms.ModelMultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        queryset=FinanceObject.objects.filter(archive=False).all()
    )

    def clean(self):
        cleaned_data = super().clean()
        fin_object = cleaned_data.get('fin_object')
        if fin_object.need_description and not cleaned_data.get('description'):
            self.add_error('description', f'Для {fin_object} необходимо указать описание')


class ReportForm(forms.ModelForm):
    class Meta:
        model = DayReport
        exclude = ["total", "total_income", "total_outcome", "rows_added"]
        widgets = {
            'p13': forms.NumberInput(attrs={
                'step': 0.5,
            }),
            'comment': forms.Textarea(attrs={
                'rows': 6,
                'cols': 80,
                'placeholder': 'Комментарий'
            }),
        }


class ReportRowForm(FinanceRowForm):
    class Meta:
        model = DayReportRow
        fields = ["total", "description"]


class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        exclude = ["total", "total_income", "total_outcome", "rows_added"]


class BudgetRowForm(FinanceRowForm):
    class Meta:
        model = BudgetRow
        fields = ["total", "description"]


class PeriodicReportForm(forms.ModelForm):
    class Meta:
        model = PeriodicReport
        fields = '__all__'
        widgets = {
            'comment': forms.Textarea(attrs={
                'rows': 6,
                'cols': 80,
                'placeholder': 'Комментарий'
            }),
        }


class NewPeriodicReportForm(forms.Form):
    date = forms.DateField(label='Дата')
    report_type = forms.ChoiceField(choices=PeriodicReport.ReportTypes.choises,
                                    label='Тип')
