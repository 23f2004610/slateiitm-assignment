from django.contrib.auth.models import AbstractUser
from django.db import models

class School(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()

    def __str__(self):
        return self.name


class Student(models.Model):
    user = models.OneToOneField(
        'User', 
        on_delete=models.CASCADE, 
        related_name='student'  # Changed from student_profile
    )
    school = models.ForeignKey(
        'School', 
        on_delete=models.CASCADE, 
        related_name='students'
    )
    date_of_birth = models.DateField()
    
    def __str__(self):
        return f"Student: {self.user.username} at {self.school.name}"


class Parent(models.Model):
    user = models.OneToOneField(
        'User', 
        on_delete=models.CASCADE, 
        related_name='parent'  # Changed from parent_profile
    )
    linked_student = models.ForeignKey(
        'Student', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='parents'
    )
    
    def __str__(self):
        return f"Parent: {self.user.username}"


class User(AbstractUser):
    ROLE_CHOICES = [
        ('school', 'School'),
        ('parent', 'Parent'),
        ('student', 'Student'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    school = models.ForeignKey(
        'School', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='users'
    )
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'role']
    
    def __str__(self):
        return f"{self.email} ({self.role})"