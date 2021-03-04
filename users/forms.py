from django import forms
from phonenumber_field.formfields import PhoneNumberField

from .models import SBFMember, Codes

class SBFSignInForm(forms.Form):
    code_parrain = forms.CharField(label='Code du Parrain', required=False, help_text='Optionnel')
    username = forms.CharField(label='Nom utilisateur', max_length=100)
    code = forms.CharField(label='Code')
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

    def clean_code_parrain(self):
        code_parrain = self.cleaned_data['code_parrain']
        codes = Codes.objects.filter(code_parrain=code_parrain)
        if codes is None:
            raise forms.ValidationError("Ce code n'existe pas")
        return code_parrain

    def clean_code(self):
        code = self.cleaned_data['code']
        try:
            SBFMember.objects.get(code=code)
        except SBFMember.DoesNotExist:
            raise forms.ValidationError('Ce code n\'existe pas')
        else:
            return code
