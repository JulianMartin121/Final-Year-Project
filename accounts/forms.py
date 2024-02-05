from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices = CustomUser.USER_TYPE_CHOICES, label = 'User Type')

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type','Uni_ID', 'password1', 'password2']
        labels = {'email': 'Email',
            'user_type': 'User Type',
            'username': 'Username',
            'Uni_ID': 'University ID',
            'password1': 'Password',
            'password2': 'Confirm Password',}
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = self.cleaned_data['user_type']
        user.email = self.cleaned_data['email']
        user.Uni_ID = self.cleaned_data['Uni_ID']

        if commit:
            print("Committed.")
            user.set_password(self.cleaned_data['password1'])
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
