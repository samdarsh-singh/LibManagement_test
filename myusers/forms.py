from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from .models import *

class UserRegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        extra_kwargs = {'password': {'write_only': True}}

class LoginForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class StudentRegisterForm(UserCreationForm):
    user = UserRegisterForm()
    class Meta:
        model = Student
        fields = '__all__'

class LibrarianRegisterForm(UserCreationForm):
    user = UserRegisterForm()
    class Meta:
        model = Librarian
        fields = '__all__'

