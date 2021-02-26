from django import forms
from django.db.models import fields
from .models import Tsv
import os

class TsvModelForm(forms.ModelForm):
    class Meta:
        model = Tsv
        fields = ('file_name',)

