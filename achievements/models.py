from django.db import models

class Achievement(models.Model):
    student = models.ForeignKey(
        'users.Student',  # Changed from User to Student model
        on_delete=models.CASCADE,
        related_name='achievements'
    )
    name = models.CharField(max_length=255)
    school = models.ForeignKey(
        'users.School',  # Added proper School relationship
        on_delete=models.CASCADE,
        related_name='achievements'
    )
    achievement_desc = models.TextField()
    date_achieved = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date_achieved']  # Most recent achievements first
        
    def __str__(self):
        return f"{self.student.user.username} - {self.name} at {self.school.name}"
    
    def clean(self):
        from django.core.exceptions import ValidationError
        # Ensure the achievement's school matches the student's school
        if self.student.school != self.school:
            raise ValidationError({
                'school': 'Achievement school must match student\'s school.'
            })
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)