from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from users.models import User, Student, Parent
from achievements.models import Achievement

@login_required
def dashboard_view(request):
    """
    Role-based dashboard rendering with a single template.
    """
    role = request.user.role
    
    # Ensure role is valid, else deny access
    if role not in ['school', 'parent', 'student']:
        raise PermissionDenied("Invalid role. Access denied.")
    
    # Prepare context data based on role
    context = {'role': role}
    
    if role == 'student':
        try:
            student = request.user.student  # Use the related_name we set up
            context['achievements'] = Achievement.objects.filter(student=student)
        except Student.DoesNotExist:
            context['achievements'] = []
    
    elif role == 'parent':
        try:
            parent = request.user.parent  # Use the related_name we set up
            if parent.linked_student:
                context['student'] = parent.linked_student
                context['achievements'] = Achievement.objects.filter(
                    student=parent.linked_student
                )
            else:
                context['achievements'] = []
        except Parent.DoesNotExist:
            context['achievements'] = []
    
    elif role == 'school':
        school = request.user.school
        if school:
            context.update({
                'total_students': Student.objects.filter(school=school).count(),
                'total_achievements': Achievement.objects.filter(school=school).count(),
                'active_parents': Parent.objects.filter(
                    linked_student__school=school
                ).count(),
            })
        else:
            context.update({
                'total_students': 0,
                'total_achievements': 0,
                'active_parents': 0,
            })
    
    return render(request, 'dashboard/role_specific_dashboard.html', context)