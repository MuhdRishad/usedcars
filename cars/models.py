from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    profile_pic = models.ImageField(upload_to="profilepics",null=True)
    phone = models.CharField(max_length=120)
    place = models.CharField(max_length=120)
    pin = models.IntegerField()
    options = (
        ("male","male"),
        ("female","female"),
        ("other","other")
    )
    gender = models.CharField(choices=options,max_length=120,default="male")
    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="users")


class Cars(models.Model):
    car_image = models.ImageField(upload_to="carimages" , null=True)
    name = models.CharField(max_length=120)
    company = models.CharField(max_length=120)
    color = models.CharField(max_length=120)
    prize = models.CharField(max_length=120)
    year = models.CharField(max_length=120)
    fuel_type = models.CharField(max_length=120)
    reason = models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name="seller")

    def __str__(self):
        return self.name

class Messages(models.Model):
    message = models.TextField(max_length=120)
    user = models.ForeignKey(User,on_delete=models.CASCADE , related_name="messager")
    reciever = models.ForeignKey(User,on_delete=models.CASCADE , related_name="reciever")


    def __str__(self):
        return self.message