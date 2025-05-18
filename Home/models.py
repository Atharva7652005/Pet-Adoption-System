from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.
class Pet_Adoption(models.Model):
    pet_name = models.CharField(max_length=50)
    pet_type = models.CharField(max_length=50)
    pet_breed = models.CharField(max_length=50)
    pet_age = models.IntegerField()
    pet_age_type = models.CharField(max_length=30,default="Young")
    pet_months = models.CharField(max_length=50)
    pet_gender = models.CharField(max_length=50)
    pet_size = models.CharField(max_length=50)
    pet_color = models.CharField(max_length=30,default="White")
    pet_background = models.TextField(default="No Information Available")
    pet_desc = models.TextField()
    pet_photo = models.ImageField(upload_to="pet_photos")
    contact_name = models.CharField(max_length=100,default="Unknown")
    contact_phoneno = models.CharField(max_length=10,default="Unknown")
    contact_email = models.EmailField(default="Unknown")
    contact_city = models.CharField(max_length=30,default="Unknown")
    timestamp = models.DateTimeField(auto_now_add=True)

class Contact_Form(models.Model):
    contact_name = models.CharField(max_length=40)
    contact_email = models.EmailField()
    contact_phoneno = models.CharField(max_length=10)
    contact_subject = models.CharField(max_length=30)
    contact_message = models.TextField()

class Add_to_Favourites(models.Model):
    fav_user = models.ForeignKey(User, on_delete=models.CASCADE)
    fav_pet = models.ForeignKey(Pet_Adoption, on_delete=models.CASCADE)

class Notifications(models.Model):
    notify_user = models.ForeignKey(User, on_delete=models.CASCADE)
    notify_pet = models.ForeignKey(Pet_Adoption, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
