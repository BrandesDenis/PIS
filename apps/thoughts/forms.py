from django import forms

from apps.thoughts.models import Thought, Topic


class ThoughtForm(forms.ModelForm):
    class Meta:
        model = Thought
        exclude = ("topics",)
        widgets = {
            'text': forms.Textarea(attrs={
                'rows': 6,
                'cols': 80,
                'placeholder': 'Содержание'
            }),
        }


class TopicRowForm(forms.Form):
    topic = forms.ModelChoiceField(Topic.objects, required=True)
