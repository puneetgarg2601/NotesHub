from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Notes, Course

class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputUsername'}),
    )
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputFirstName'}),
    )
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'id': 'InputLastName'}),
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'id': 'InputEmail'}),
        help_text="Enter your iitb email address",
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'id': 'InputPassword'}),
    )

    def clean_email(self):
        email = self.cleaned_data['email']
        domain = email.split('@')[-1]

        # Ensure email ends with 'iitb.ac.in'
        if domain != 'iitb.ac.in':
            raise ValidationError("Email domain must be 'iitb.ac.in'")
        
        # Ensure email is unique
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email is already registered.")
        
        return email

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.strip():
            raise ValidationError("First name cannot be empty.")
        return first_name
    
class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        label='Username'
    )
    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        label='Password'
    )

class CreateNoteForm(forms.Form):
    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter title'
        })
    )
    description = forms.CharField(
        required=True,
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Enter description',
            'rows': 5
        })
    )
    file = forms.FileField(
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    course_code = forms.ModelChoiceField(
        queryset=Course.objects.values_list('course_code', flat=True),
        required=True,
        widget=forms.Select(attrs={'class': 'form-control'})
    )