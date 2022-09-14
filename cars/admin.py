from django.contrib import admin
from cars.models import Cars,UserProfile,Messages

# Register your models here.

admin.site.register(Cars)
admin.site.register(UserProfile)
admin.site.register(Messages)