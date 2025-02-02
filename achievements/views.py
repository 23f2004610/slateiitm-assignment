from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Achievement
from .serializers import AchievementSerializer
from users.permissions import RoleBasedPermission

class AchievementViewSet(viewsets.ModelViewSet):
    """
    ViewSet for managing student achievements with role-based access control.
    """
    serializer_class = AchievementSerializer
    permission_classes = [permissions.IsAuthenticated, RoleBasedPermission]
    allowed_roles = ['school', 'parent', 'student']

    def get_queryset(self):
        """
        Restrict achievements based on user role:
        - Students can only view their own achievements.
        - Parents can only view their linked student's achievements.
        - Schools can view all achievements.
        """
        user = self.request.user
        student_id = self.kwargs.get('student_id')

        # Schools can access all achievements
        if user.role == 'school':
            return Achievement.objects.all()

        # Ensure student_id is provided and is valid
        if not student_id:
            raise PermissionDenied("Student ID is required to fetch achievements.")

        try:
            student_id = int(student_id)
        except ValueError:
            raise PermissionDenied("Invalid student ID format.")

        # Students can only view their own achievements
        if user.role == 'student':
            if student_id != user.id:
                raise PermissionDenied("You can only view your own achievements.")
            return Achievement.objects.filter(student_id=user.id)

        # Parents can only view their linked student's achievements
        if user.role == 'parent':
            if not user.linked_student_id or student_id != user.linked_student_id:
                raise PermissionDenied("You can only view your linked student's achievements.")
            return Achievement.objects.filter(student_id=user.linked_student_id)

        return Achievement.objects.none()
