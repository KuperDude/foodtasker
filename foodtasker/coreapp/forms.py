from multiprocessing import AuthenticationError
from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User 
from .models import Restaurant, Meal, Order, GeoJsonFile
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

class GeoJsonFileForm(forms.ModelForm):
    class Meta:
        model = GeoJsonFile
        fields = ['file']

    def __init__(self, *args, **kwargs):
        super(GeoJsonFileForm, self).__init__(*args, **kwargs)
        self.fields['file'].widget.attrs.update({'id': 'geojson-content'})

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Проверка MIME-типа
            if file.content_type != 'application/geo+json':
                raise ValidationError('Пожалуйста, загрузите файл в формате GeoJSON.')

            # Альтернативная проверка по расширению (если нужно)
            if not file.name.endswith('.geojson'):
                raise ValidationError('Файл должен иметь расширение .geojson.')
        return file
