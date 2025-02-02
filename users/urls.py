from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, RegisterAPIView, CustomTokenObtainPairView, CustomTokenRefreshView, PasswordResetView, PasswordResetConfirmView, CustomLogoutView


urlpatterns = [
    # Authentication endpoints
    path("register/", RegisterView.as_view(), name="register"),  # Renders register HTML page
    path("login/", LoginView.as_view(), name="login"),  # Renders login HTML page
    path('logout/', CustomLogoutView.as_view(), name='logout'),  # Logs out the user
    path("api/register/", RegisterAPIView.as_view(), name="api_register"),  # JSON-based API registration
    path("api/login/", CustomTokenObtainPairView.as_view(), name="api_login"),  # API-based JWT login
    path("api/token/refresh/", CustomTokenRefreshView.as_view(), name="api_token_refresh"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('password-reset/', PasswordResetView.as_view(), name='password_reset'),
    path('password-reset-confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),

    # User profile
    # path('profile/', UserProfileView.as_view(), name='user-profile'),
]
