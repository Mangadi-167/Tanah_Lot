# dashboard/forms.py
from django.contrib.auth.forms import PasswordChangeForm
from django import forms
from django.contrib.auth.models import User
from .models import Content, CONTENT_TYPE_CHOICES, ROLE_CHOICES
from .models import Event

# ===================================================================
# DEFINISI KELAS CSS (AGAR TAMPILAN TIDAK RUSAK)
# ===================================================================
FORM_INPUT_CLASS = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-pr-900 focus:border-pr-900 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-pr-900 dark:focus:border-pr-900'
SELECT_INPUT_CLASS = 'bg-gray-50 border font-se border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-pr-900 focus:border-pr-900 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-pr-900 dark:focus:border-pr-900'
TEXTAREA_CLASS = 'block p-2.5 w-full text-sm text-gray-900 bg-gray-50 rounded-lg border border-gray-300 focus:ring-pr-900 focus:border-blue-500 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-pr-900 dark:focus:border-pr-900'
IMAGE_INPUT_CLASS = 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400'
TEXT_INPUT_CLASS = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-pr-900 focus:border-pr-900 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-pr-900 dark:focus:border-pr-900'
FORM_RESET_PASSWORD = 'bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-pr-900 focus:border-pr-900 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-pr-900 dark:focus:border-pr-900'
# ==================================
# FORM 1: UNTUK CONTENT
# ==================================
class ContentForm(forms.ModelForm):
    content_type = forms.ChoiceField(
        choices=[('', '-- Select content type --')] + CONTENT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': SELECT_INPUT_CLASS})
    )

    class Meta:
        model = Content
        fields = ['title', 'description', 'image', 'content_type']
        widgets = {
            'title': forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Enter a content title'}),
            'description': forms.Textarea(attrs={'class': TEXTAREA_CLASS, 'rows': 4, 'placeholder': 'Enter a content description'}),
            'image': forms.ClearableFileInput(attrs={'class': IMAGE_INPUT_CLASS})
        }

    def _init_(self, *args, **kwargs):
        super(ContentForm, self)._init_(*args, **kwargs)
        self.fields['title'].label = "Name"
        self.fields['description'].label = "Description"
        self.fields['image'].label = "Gambar"
        self.fields['content_type'].label = "Content Type"


# ===================================================================
# FORM 2: UNTUK ADMIN MENAMBAHKAN USER BARU
# ===================================================================
class UserCreationFormByAdmin(forms.Form):
    username = forms.CharField(label="Name", max_length=150, widget=forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Enter a username'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Enter email'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Enter password'}))
    phone_number = forms.CharField(label="Phone Number", max_length=20, required=False, widget=forms.TextInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Enter a phone number'}))
    role = forms.ChoiceField(label="User Position", choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': SELECT_INPUT_CLASS}))

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username ini sudah digunakan.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email ini sudah digunakan oleh akun lain.")
        return email


# ===================================================================
# FORM 3: UNTUK ADMIN MEMPERBARUI USER
# (Ini diletakkan di luar, sejajar dengan dua form lainnya)
# ===================================================================
class UpdateUserForm(forms.Form):
    username = forms.CharField(label="Name", max_length=150, widget=forms.TextInput(attrs={'class': FORM_INPUT_CLASS}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': FORM_INPUT_CLASS}))
    phone_number = forms.CharField(label="Phone Number", max_length=20, required=False, widget=forms.TextInput(attrs={'class': FORM_INPUT_CLASS}))
    role = forms.ChoiceField(label="User Position", choices=ROLE_CHOICES, widget=forms.Select(attrs={'class': SELECT_INPUT_CLASS}))
    password = forms.CharField(label='New Password (Opsional)', required=False, widget=forms.PasswordInput(attrs={'class': FORM_INPUT_CLASS, 'placeholder': 'Kosongkan jika tidak diubah'}))

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.pop('instance', None)
        super(UpdateUserForm, self).__init__(*args, **kwargs)

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if self.instance and User.objects.filter(username=username).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Username ini sudah digunakan oleh user lain.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if self.instance and User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Email ini sudah digunakan oleh user lain.")
        return email
    


class PasswordResetFormByAdmin(forms.Form):
    # Field untuk password baru
    new_password1 = forms.CharField(
        label="Password Baru", 
        widget=forms.PasswordInput(attrs={'class': FORM_RESET_PASSWORD, 'placeholder': 'Masukkan password baru'}),
        help_text="Password harus memiliki setidaknya 8 karakter."
    )
    # Field untuk konfirmasi password baru
    new_password2 = forms.CharField(
        label="Konfirmasi Password Baru", 
        widget=forms.PasswordInput(attrs={'class': FORM_RESET_PASSWORD, 'placeholder': 'Ketik ulang password baru'})
    )

    # Fungsi validasi untuk memastikan kedua password cocok
    def clean_new_password2(self):
        cd = self.cleaned_data
        if cd['new_password1'] and cd['new_password2'] and cd['new_password1'] != cd['new_password2']:
            raise forms.ValidationError("Password tidak cocok.")
        return cd['new_password2']
    

# Calender
class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['event_date', 'event_name', 'description']
        widgets = {
            'event_date': forms.DateInput(
                # Memaksa format input dan output HTML menjadi YYYY-MM-DD
                format='%Y-%m-%d',
                attrs={
                    # Gunakan input tanggal asli dari browser
                    'type': 'date',
                    'class': 'font-se bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-pr-900 focus:border-pr-900 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-pr-900 dark:focus:border-pr-900',
                }
            ),
            'event_name': forms.TextInput(attrs={'class': '... class styling Anda ...'}),
            'description': forms.Textarea(attrs={'class': '... class styling Anda ...', 'rows': 4}),
        }