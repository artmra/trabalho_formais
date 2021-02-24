from django import forms


class InputForm(forms.Form):
    content = forms.CharField(label=False, required=False, widget=forms.Textarea(attrs={
        'cols': '40',
        'rows': '20',
    }))


class GrammarForm(InputForm):
    pass
