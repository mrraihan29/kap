
#from django import forms
#from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#from .models import CustomUser

#class SignUpForm(UserCreationForm):
    #email = forms.EmailField(max_length=200, help_text='Required')

    #class Meta:
        #model = CustomUser
        #fields = ('username', 'email', 'password1', 'password2')

#class LoginForm(AuthenticationForm):
    #username = forms.CharField(max_length=100)
    #password = forms.CharField(widget=forms.PasswordInput())


from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class SignUpForm(UserCreationForm):
    email = forms.EmailField(
        max_length=200, 
        help_text='Wajib diisi. Masukkan alamat email yang valid.',
        label='Alamat Email'
    )
    username = forms.CharField(
        max_length=100,
        help_text='Gunakan 150 karakter atau kerang dengan hanya huruf, angka, dan @/./+/-/_ saja.',
        label='Nama Pengguna'
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(),
        help_text=(
            'Wajib diisi. Masukkan kata sandi.'
            '<ul>'
            '<li>Mengandung huruf besar dan kecil</li>'
            '<li>Mengandung angka</li>'
            '<li>Mengandung karakter spesial (misalnya @, #, $)</li>'
            '</ul>'
        ),
        label='Kata Sandi'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(),
        help_text='Wajib diisi. Masukkan ulang kata sandi untuk konfirmasi.',
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