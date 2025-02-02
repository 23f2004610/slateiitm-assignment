from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

User = get_user_model()

# 🔹 Registration Form
class RegisterForm(UserCreationForm):
    """
    Custom user registration form with role selection.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = """Your password can't be too similar to your other personal information.
            Your password must contain at least 8 characters.
            Your password can't be a commonly used password.
            Your password can't be entirely numeric.
        """

    ROLE_CHOICES = [
        ('school', 'School'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    ]
    
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, label="User Role")

    class Meta:
        model = User
        fields = ['username', 'email', 'role', 'password1', 'password2']

    def save(self, commit=True):
        """
        Save the user instance with the selected role.
        """
        user = super().save(commit=False)
        user.role = self.cleaned_data['role']
        if commit:
            user.save()
        return user


# 🔹 Login Form (Using Django's Built-in AuthenticationForm)

class LoginForm(AuthenticationForm):
    # role = forms.ChoiceField(choices=[('school', 'School'), ('parent', 'Parent'), ('student', 'Student')])

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})
        self.fields['password'].widget.attrs.update({'class': 'w-full px-3 py-2 border border-gray-300 rounded-md'})

