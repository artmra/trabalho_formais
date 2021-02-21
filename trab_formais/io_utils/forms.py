from django import forms
from .models import FiniteAutomata


class FiniteAutomataForm(forms.Form):
    content = forms.CharField(label=False, required=False, widget=forms.Textarea(attrs={
        'cols': '40',
        'rows': '20',
    }))


class RegularExpressionForm(forms.Form):
    content = forms.CharField(label=False, required=False, widget=forms.Textarea(attrs={
        'cols': '40',
        'rows': '20',
    }))
