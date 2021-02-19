from django import forms
from .models import FiniteAutomata


class UploadFileForm(forms.Form):
    afFileInput = forms.FileField()
