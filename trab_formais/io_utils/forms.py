from django import forms
from .models import FiniteAutomata


class InputForm(forms.Form):
    content = forms.CharField(label=False, required=False, widget=forms.Textarea(attrs={
        'cols': '40',
        'rows': '20',
    }))
