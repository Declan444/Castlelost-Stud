from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Instructor(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)

class LessonType(models.Model):
    LEVEL_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    level = models.CharField(max_length=20, choices=LEVEL_CHOICES)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='lesson_types')
    content = models.TextField()


