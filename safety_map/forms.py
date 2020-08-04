from django import forms
from .models import Danger

class DangerForm(forms.ModelForm):
    class Meta:
        model = Danger
        fields = ['danger_type','danger_img','danger_loc']
