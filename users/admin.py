# admin.py in your app folder
from django.contrib import admin
from .models import User, Student, Parent, School  # Add all your models here

admin.site.register(User)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(School)
