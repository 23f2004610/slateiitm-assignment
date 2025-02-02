from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from users.models import User

class AuthenticationTests(APITestCase):
    def setUp(self):
        self.user_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'testpass123',
            'role': 'student'
        }
        self.user = User.objects.create_user(**self.user_data)

    def test_login(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
            'role': self.user_data['role']
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_invalid_role_login(self):
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {
            'username': self.user_data['username'],
            'password': self.user_data['password'],
            'role': 'parent'  # Wrong role
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class AchievementTests(APITestCase):
    def setUp(self):
        # Create test users and achievements
        self.student = User.objects.create_user(
            username='student',
            password='pass123',
            role='student'
        )
        self.parent = User.objects.create_user(
            username='parent',
            password='pass123',
            role='parent',
            linked_student=self.student
        )
        self.achievement = Achievement.objects.create(
            student=self.student,
            name='Test Achievement',
            school_name='Test School'
        )

    def test_student_can_view_own_achievements(self):
        self.client.force_authenticate(user=self.student)
        url = reverse('achievement-list', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_parent_can_view_linked_student_achievements(self):
        self.client.force_authenticate(user=self.parent)
        url = reverse('achievement-list', kwargs={'student_id': self.student.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)