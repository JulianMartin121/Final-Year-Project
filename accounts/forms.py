from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import CustomUser

# Registration forms for student and teacher
class StudentRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        #Labels for the form fields to make them more user friendly
        labels = {'email': 'Email',
                  'password1': 'Password',
                  'password2': 'Confirm Password',
                  'username': 'Username'}
    
    def save(self, commit=True):
        user = super(StudentRegistrationForm, self).save(commit=False)
        user.user_type = 1 # Set the user type to student
        if commit:
            user.save()
        return user
    
class TeacherRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2']
        labels = {'email': 'Email',
                  'password1': 'Password',
                  'password2': 'Confirm Password',
                  'username': 'Username'}
    
    
    def save(self, commit=True):
        user = super(TeacherRegistrationForm, self).save(commit=False)
        user.user_type = 2 # Set the user type to teacher
        user.is_staff = True # Set the user to be a staff member
        user.is_superuser = True # Set the user to be a superuser
        if commit:
            user.save()
        return user

# Login forms for student and teacher
class StudentLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        labels = {'username': 'Username',
                  'password': 'Password'}

class TeacherLoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']
        labels = {'username': 'Username',
                  'password': 'Password'}
