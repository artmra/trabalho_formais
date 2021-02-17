from django import forms
from .models import AF

class UploadFileForm(forms.Form):
    afFileInput = forms.FileField()