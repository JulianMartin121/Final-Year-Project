from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

class RegistrationForm(UserCreationForm):
    USER_TYPE_CHOICES = (
        (1, 'student'),
        (2, 'teacher'),
    )

    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, required=True)

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
        user = super(RegistrationForm, self).save(commit=False)
        user.user_type = self.cleaned_data['user_type']

        if user.user_type == '1':
            user.user_type = 1 # Set user to student
            user.studentID = self.cleaned_data['Uni_ID']
        elif user.user_type == '2':
            user.user_type = 2 # Set user to teacher
            user.teacherID = self.cleaned_data['Uni_ID']

        if commit:
            user.save()
        return user

class LoginForm(AuthenticationForm):
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
