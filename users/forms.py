from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import CashFoodMember 

class CashFoodSignInForm(forms.Form):
    username = forms.CharField(label='Nom utilisateur', max_length=100)
    code = forms.CharField(label='Code du Parrain')
    email = forms.EmailField(max_length=255, required=False, label='Email')
    phone_number = PhoneNumberField()
    password = forms.CharField(label='Mot de Passe', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='Confirmer le mot de passe', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password == confirm_password:
            return confirm_password
        raise forms.ValidationError('Les mots de passe ne sont pas identiques')

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            CashFoodMember.objects.get(code=code)
        except CashFoodMember.DoesNotExist:
            raise forms.ValidationError('Ce code n\'existe pas')
        else:
            return code


    