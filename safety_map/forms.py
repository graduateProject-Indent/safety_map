from django import forms
from .models import Danger

from django.forms.models import modelform_factory
)

class DangerForm(forms.ModelForm): #create view
    class Meta:
        model = Danger
        fields = ['danger_type','danger_img','danger_loc']


