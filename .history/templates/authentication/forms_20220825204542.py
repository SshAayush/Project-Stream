from django import forms
from .models import MyModel

class MyForm(forms.ModelForm):
  class Meta:
    model = MyModel
    fields = ["html_email"]
    labels = {'html_email'}