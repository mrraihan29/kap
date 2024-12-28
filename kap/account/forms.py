from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200, 
        help_text='Masukkan alamat email yang sesuai.',
        label='Alamat Email'
    )
    username = forms.CharField(
        max_length=100,
        help_text='Gunakan maks. 150 karakter dan tanpa spasi.',
        label='Nama Pengguna'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        help_text=(
            'Masukkan kata sandi yang menggunakan:'
            '<ul>'
            '<li>Huruf besar dan kecil.</li>'
            '<li>Angka.</li>'
            '<li>karakter spesial (misal: @, #, $).</li>'
            '</ul>'
        ),
        label='Kata Sandi'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        help_text='Masukkan ulang kata sandi.',
        label='Konfirmasi Kata Sandi'
    )

    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=100, 
        label='Nama Pengguna'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(),
        label='Kata Sandi'
    )