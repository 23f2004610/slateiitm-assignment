# admin.py in your app folder
from django.contrib import admin
from .models import Achievement

admin.site.register(Achievement)
