from django.contrib import admin
from django import forms
from .models import Restaurant, Customer, Driver, Meal, Order, OrderDetails, Category, Ingredient, GeoJsonFile, RestaurantMeal, Cashier
from django.contrib.auth.models import User


class RestaurantAdminForm(forms.ModelForm):
    class Meta:
        model = Restaurant
        fields = '__all__'
    
    # Переопределяем поле пользователя
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_staff=True)

class RestaurantAdmin(admin.ModelAdmin):
    form = RestaurantAdminForm

class CashierAdminForm(forms.ModelForm):
    class Meta:
        model = Cashier
        fields = '__all__'
    
    # Переопределяем поле пользователя
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user'].queryset = User.objects.filter(is_staff=True)

class CashierAdmin(admin.ModelAdmin):
    form = CashierAdminForm

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    list_editable = ('order',)
    
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Cashier, CashierAdmin)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Ingredient)
admin.site.register(GeoJsonFile)
admin.site.register(RestaurantMeal)