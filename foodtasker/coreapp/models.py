from django.db import models
from django.contrib.auth.models import User
from cloudinary.models import CloudinaryField

class Restaurant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='restaurant')
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    logo = CloudinaryField('image')

    def __str__(self):
        return self.name



