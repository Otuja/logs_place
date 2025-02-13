from django import forms
from .models import SocialAccount


class SocialAccountForm(forms.ModelForm):
    class Meta:
        model = SocialAccount
        fields = ['platform', 'username', 'email', 'password', 'followers_count', 'is_verified', 'price', 'url', 'description']
        
        widgets = {
            'platform': forms.Select(attrs={'class': 'border border-orange-50 rounded-lg p-2 w-full'}),
            'username': forms.TextInput(attrs={'class': 'border border-orange-50 rounded-lg p-2 w-full'}),
            'email': forms.EmailInput(attrs={'class': 'border border-orange-50 rounded-lg p-2 w-full'}),
            'password': forms.PasswordInput(attrs={'class': 'border border-orange-50 rounded-lg p-2 w-full'}),
            'followers_count': forms.NumberInput(attrs={'class': 'border border-orange-50 rounded-lg p-2 w-full'}),
            'is_verified': forms.CheckboxInput(attrs={'class': 'form-checkbox h-5 w-5 text-orange-500'}),
            'price': forms.NumberInput(attrs={'class': 'border border-orange-50 rounded-lg p-2 w-full'}),
            'url': forms.URLInput(attrs={'class': 'border border-orange-50 rounded-lg p-2 w-full'}),
            'description': forms.Textarea(attrs={'class': 'border border-orange-50 rounded-lg p-2 w-full', 'rows': 3}),
        }


