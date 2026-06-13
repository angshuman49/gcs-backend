from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    school = models.CharField(max_length=200, blank=True)
    class_grade = models.CharField(max_length=50, blank=True)
    ROLE_CHOICES = [
        ('participant', 'Participant'),
        ('executive', 'Executive'),
    ]
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='participant')