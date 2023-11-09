from django.contrib import admin
from .models import Restaurant, Customer, Driver, Meal, Order, OrderDetails, Category, Ingredient

admin.site.register(Restaurant)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Meal)
admin.site.register(Order)
admin.site.register(OrderDetails)
admin.site.register(Category)
admin.site.register(Ingredient)