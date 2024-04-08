from multiprocessing import AuthenticationError
from django import forms
from django.contrib.auth.models import User 
from .models import Restaurant, Meal, Order
from django.contrib.auth.forms import (
    AuthenticationForm,
)

class UserForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User 
        fields = ('email', 'username',)
        # fields = ('username', 'password', 'first_name', 'last_name', 'email')


class RestaurantForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = ('name', 'phone', 'address', 'logo')

class AccountForm(forms.ModelForm):
    email = forms.CharField(max_length=100, required=True)

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email")
        labels = {'first_name': 'Имя', 'last_name': 'Фамилия', 'email': 'Почта'}

class MealForm(forms.ModelForm):
    class Meta:
        model = Meal
        exclude = ('restaurant',)

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("status",)
        labels = {'status': ' ',}

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': ''}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': ''}))
 
    class Meta:
        model = User
        fields = ('username', 'password',)
        labels = {'username': ' ', 'password': ' '}