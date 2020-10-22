from django import forms

from apps.thoughts.models import Thought, Topic


class ThoughtForm(forms.ModelForm):
    class Meta:
        model = Thought
        exclude = ("topics",)


class TopicRowForm(forms.Form):
    topic = forms.ModelChoiceField(Topic.objects.all(), required=True)
