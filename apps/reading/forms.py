from django import forms

from apps.reading.models import Reading


class ReadingForm(forms.ModelForm):
    class Meta:
        model = Reading
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 10, 'cols': 80}),
        }
