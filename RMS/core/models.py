from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = [
        ("college_admin", "College Admin"),
        ("department_admin", "Department Admin"),
    ]

    role = models.CharField(
        max_length=50,
        choices=ROLE_CHOICES
    )
    Department_choices = [
        ("CSE", "Computer Science and Engineering"),
        ("BBA", "Business Administration"),
        ("English", "English"),
        ("Bangla", "Bangla"),
        ("Economics", "Economics"),
        ("Social Work", "Social Work"),
        ("Political Science", "Political Science"),
        ("Islamic History & Culture", "Islamic History & Culture"),
        ("Accounting", "Accounting"),
        ("Finance and Banking", "Finance and Banking"),
        ("Management", "Management"),
        ("Mathematics", "Mathematics"),
        ("Physics", "Physics"),
        ("Chemistry", "Chemistry"),
        ("Anthropology", "Anthropology"),
        ("Inter-Science", "Inter-Science"),
        ("Inter-Commerce", "Inter-Commerce"),
        ("Inter-Arts", "Inter-Arts"),
        ("All", "All"),
    ]
    department = models.CharField(
        max_length=100,
        choices=Department_choices,
        default="All"
    )

    def __str__(self):
        return self.username

class Student(models.Model):
    student_name = models.CharField(max_length=150)
    student_roll = models.CharField(max_length=20)
    department = models.CharField(max_length=100, choices=User.Department_choices)
    session = models.CharField(max_length=20)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['student_roll', 'department'], name='unique_student_department_roll')
        ]

    def __str__(self):
        return f"{self.student_name} - {self.student_roll}"