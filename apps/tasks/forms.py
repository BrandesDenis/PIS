from django import forms

from apps.tasks.models import Task


class DateInput(forms.DateInput):
    input_type = 'date'


class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
            'start': DateInput(),
            'end': DateInput(),
        }
