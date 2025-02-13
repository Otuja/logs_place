from django import forms
from .models import Wallet


class NINForm(forms.ModelForm):
    class Meta:
        model = Wallet
        fields = ["nin"]
        widgets = {
            "nin": forms.TextInput(attrs={"class": "form-control", "placeholder": "Enter your 11-digit NIN"})
        }
