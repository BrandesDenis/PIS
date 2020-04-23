from django.forms import ModelForm
from finance.models import DayReport, DayReportRow


class ReportForm(ModelForm):
    class Meta:
        model = DayReport
        exclude = ['total']


class ReportRowForm(ModelForm):
    class Meta:
        model = DayReportRow
        fields = ['fin_object', 'total']
