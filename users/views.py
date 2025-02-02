from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import CreateView, FormView
from django.urls import reverse_lazy
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.views import LogoutView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status, generics
from django.contrib.auth import get_user_model
from .forms import RegisterForm, LoginForm
from .serializers import (
    CustomTokenObtainPairSerializer, UserSerializer,
    PasswordResetSerializer, PasswordResetConfirmSerializer
)

User = get_user_model()


# 🔹 User Registration View (Class-Based)
class RegisterView(FormView):
    template_name = "users/register.html"
    form_class = RegisterForm
    success_url = reverse_lazy("dashboard")  # Redirect after successful registration

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)  # Log in the user automatically after registration
        return super().form_valid(form)

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))


# 🔹 User Login View (Class-Based)
class LoginView(FormView):
    template_name = "users/login.html"
    form_class = LoginForm
    success_url = reverse_lazy("dashboard")  # Redirect after successful login

    def form_valid(self, form):
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)

        if user is not None:
            login(self.request, user)
            return super().form_valid(form)
        else:
            messages.error(self.request, "Invalid username or password.")
            return self.form_invalid(form)



class CustomLogoutView(LogoutView):
    """
    A custom logout view to handle user logout functionality.
    """
    next_page = reverse_lazy('login')  # Redirect to login page after logout

    def get(self, request, *args, **kwargs):
        """
        Handle GET request to logout and redirect to the login page.
        """
        logout(request)
        return redirect(self.next_page)
    

# 🔹 API-Based Registration (JSON Response)
class RegisterAPIView(generics.CreateAPIView):
    """
    Handles user registration via API (JSON response).
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()
        return Response(
            {
                "message": "User registered successfully",
                "user": UserSerializer(user).data,
            },
            status=status.HTTP_201_CREATED,
        )



# 🔹 Custom Login View (Role-Based)
class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom login view with JWT and role validation.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Authenticate user and return JWT token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# 🔹 JWT Token Refresh View
class CustomTokenRefreshView(TokenRefreshView):
    """
    Handles JWT token refresh.
    """
    pass  # Uses default behavior from SimpleJWT


# 🔹 Password Reset Request View
class PasswordResetView(generics.GenericAPIView):
    """
    Request a password reset email.
    """
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Sends a password reset email with a secure token.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        # Generate password reset token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        reset_link = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}"

        # Send password reset email
        send_mail(
            subject="Password Reset Request",
            message=f"Click the link to reset your password: {reset_link}",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
            fail_silently=False,
        )

        return Response({"message": "Password reset link sent."}, status=status.HTTP_200_OK)


# 🔹 Password Reset Confirmation View
class PasswordResetConfirmView(generics.GenericAPIView):
    """
    Confirm and reset the password using token and UID.
    """
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        """
        Verifies the reset token and updates the user's password.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response({"message": "Password reset successful."}, status=status.HTTP_200_OK)
