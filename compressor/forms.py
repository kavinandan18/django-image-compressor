from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'}),
        label='Confirm Password'
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords do not match.")
        return password2


class ImageUploadForm(forms.Form):
    image = forms.ImageField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    size_kb = forms.IntegerField(label='Desired Size (KB)', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    quality = forms.IntegerField(label='Quality (1-100)', min_value=1, max_value=100, widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean_quality(self):
        quality = self.cleaned_data.get('quality')
        if quality < 1 or quality > 100:
            raise forms.ValidationError("Quality must be between 1 and 100.")
        return quality

class FileUploadForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    size_kb = forms.IntegerField(label='Desired Size (KB)', widget=forms.NumberInput(attrs={'class': 'form-control'}))
    
    def clean_size_kb(self):
        size_kb = self.cleaned_data.get('size_kb')
        if size_kb <= 0:
            raise forms.ValidationError("Size must be greater than 0 KB.")
        return size_kb
