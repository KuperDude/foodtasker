from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField
from django.utils import timezone

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=255, verbose_name='Название')
    phone = models.CharField(max_length=255, verbose_name='Телефон')
    address = models.CharField(max_length=255, verbose_name='Адрес')
    logo = CloudinaryField('image')

    def __str__(self):
        return self.name

class Customer(models.Model):
    user = models.OneToOneField(User, unique=True, on_delete=models.CASCADE, related_name='customer')
    avatar = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=255, blank=True)
    address = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Driver(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='driver')
    avatar = models.CharField(max_length=255, blank=True)
    car_model = models.CharField(max_length=255)
    plate_number = models.CharField(max_length=255, blank=True)
    location = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return self.user.get_full_name()

class Cashier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} - {self.restaurant.name}"

class Category(models.Model):
    name = models.CharField(max_length=255, default='SOME STRING')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.name

class Ingredient(models.Model):
    name = models.CharField(max_length=255, default='SOME STRING')
    image = CloudinaryField('image')
    
    def __str__(self):
        return self.name

class Meal(models.Model):
    restaurants = models.ManyToManyField(Restaurant, through='RestaurantMeal', related_name='meals')
    category = models.ForeignKey(Category, null=True, on_delete=models.CASCADE, related_name='meal', verbose_name="Категория")
    ingredients = models.ManyToManyField(Ingredient, null=True, related_name='meal', verbose_name="Ингредиенты")
    name = models.CharField(max_length=255, verbose_name="Название")
    short_description = models.TextField(max_length=500, verbose_name="Описание")
    image = CloudinaryField('image')
    price = models.IntegerField(default=0, verbose_name="Цена")

    def __str__(self):
        return self.name 

class RestaurantMeal(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    price = models.IntegerField(default=0, verbose_name="Цена")
    is_available = models.BooleanField(default=True, verbose_name="Наличие товара")

    class Meta:
        unique_together = ('restaurant', 'meal')

    def __str__(self):
        return f'{self.restaurant.name} - {self.meal.name} : {self.price}'

class Order(models.Model):
    CANCELLED = 0
    PROCESSING = 1
    COOKING = 2
    READY = 3
    ONTHEWAY = 4
    DELIVERED = 5

    STATUS_CHOICES = (
        (CANCELLED, 'Отменен'),
        (PROCESSING, 'В обработке'),
        (COOKING, 'Готовиться'), 
        (READY, 'Готов к отправке'), 
        (ONTHEWAY, 'В пути'), 
        (DELIVERED, 'Доставлен'), 
    )

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT)
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=500)
    total = models.IntegerField()
    status = models.IntegerField(choices=STATUS_CHOICES)
    created_at = models.DateTimeField(default=timezone.now)
    picked_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

class OrderDetails(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name='order_details')
    meal = models.ForeignKey(Meal, on_delete=models.PROTECT)
    quantity = models.IntegerField()
    sub_total = models.IntegerField()

    def __str__(self):
        return str(self.id)

class GeoJsonFile(models.Model):
    file = models.FileField(upload_to='geojson/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"GeoJSON файл от {self.uploaded_at}"

        