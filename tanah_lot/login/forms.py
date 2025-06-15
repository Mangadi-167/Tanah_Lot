# login/forms.py

from django import forms
from django.contrib.auth.models import User

# ===================================================================
# DEFINISIKAN KELAS CSS DI SINI (DI LUAR KELAS)
# ===================================================================

FORM_INPUT_CLASS = 'bg-gray-50 border border-gray-300 text-gray-900 rounded-lg focus:ring-pr-900 focus:border-pr-900 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500'


# ===================================================================
# FORM LOGIN (SIGN IN)
# ===================================================================
class LoginForm(forms.Form):
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={
            'class': FORM_INPUT_CLASS,
            'placeholder': 'Enter email',
            'required': True
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': FORM_INPUT_CLASS,
            'placeholder': 'Enter password',
            'required': True
        })
    )

# ===================================================================
# FORM REGISTRASI (SIGN UP)
# ===================================================================
class RegistrationForm(forms.ModelForm):
   
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Enter password', 'required': True}))
    password2 = forms.CharField(label='Konfirmasi Password', widget=forms.PasswordInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Confirm password', 'required': True}))
    phone_number = forms.CharField(label='Phone Number', max_length=20, required=False, widget=forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Enter a phone number'}))

    class Meta:
        model = User
        fields = ('username', 'email')
        widgets = {
             'username': forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Enter a username', 'required': True}),
             'email': forms.EmailInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Enter email', 'required': True}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password2') and cd['password'] != cd['password2']:
            raise forms.ValidationError('Password tidak cocok.')
        return cd.get('password2')
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ini sudah digunakan oleh akun lain.")
        return email 