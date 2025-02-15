from django import forms
from .models import Wallet

class NINForm(forms.ModelForm):
    nin = forms.CharField(
        max_length=11,
        min_length=11,
        label="National Identification Number (NIN)",
        widget=forms.TextInput(attrs={
            'class': 'form-input',
            'placeholder': 'Enter your 11-digit NIN',
            'pattern': '[0-9]{11}',  # Ensures only digits are entered
            'title': 'NIN must be exactly 11 digits'
        })
    )

    class Meta:
        model = Wallet
        fields = ['nin']
