from django.db import models
from django.contrib.auth.models import AbstractUser
from enum import Enum

# Enum for User Roles
class Role(Enum):
    STUDENT = 'Student'
    TEACHER = 'Teacher'
    ADMIN = 'Admin'

# Custom User model
class CustomUser(AbstractUser):
    # Add a role field that uses the Role Enum
    role = models.CharField(
        max_length=10,
        choices=[(role.name, role.value) for role in Role],
        default=Role.STUDENT.name
    )

    def __str__(self):
        return f"{self.username} ({self.role})"
