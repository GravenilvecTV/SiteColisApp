from django import forms 
from .models import Parcel

class RegisterParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['adress_dep', 'adress_arr', 'weight']