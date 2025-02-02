from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AchievementViewSet

# Using Django REST framework's router for API views
router = DefaultRouter()
router.register(r'achievements', AchievementViewSet, basename='achievement')

urlpatterns = [
    path('', include(router.urls)),  # Includes all API routes for achievements
]
