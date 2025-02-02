"""
URL configuration for slate project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path, include
from django.contrib import admin
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from users.views import CustomTokenObtainPairView
from achievements.views import AchievementViewSet
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

router = DefaultRouter()
router.register(r'achievements/student/(?P<student_id>\d+)', AchievementViewSet, basename='achievement')



schema_view = get_schema_view(
   openapi.Info(
      title="Slate API",
      default_version='v1',
      description="API documentation for Slate's Role-Based Authentication System",
      terms_of_service="https://www.slateiitm.com/terms/",
      contact=openapi.Contact(email="contact@slateiitm.com"),
      license=openapi.License(name="MIT License"),
   ),
   public=True,
   permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
    # path('auth/password/reset/', PasswordResetView.as_view(), name='password_reset'),
    # path('auth/password/reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    # API routes
    path('users/', include('users.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('api/', include('achievements.urls')),  # Achievements are under 'api/'
]