from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Instructor(models.Model):
    name = models.CharField(max_length=200)
    bio = models.TextField()
    slug = models.SlugField(max_length=200, unique=True)
    updated_on = models.DateTimeField(auto_now=True)

class LessonType(models.Model):
    LESSON_CHOICES = (
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    )

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    lesson_choices = models.CharField(max_length=20, choices=LESSON_CHOICES)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE, related_name='lesson_types')
    content = models.TextField()
    excerpt = models.TextField(blank=True)

class LessonDate(models.Model):
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    slug = models.SlugField(unique=True, blank=True)

class BookingDate(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending Approval'),
        ('approved', 'Approved'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson_date = models.ForeignKey(LessonDate, on_delete=models.CASCADE)
    lesson_type = models.ForeignKey(LessonType, on_delete=models.CASCADE)
    instructor = models.ForeignKey(Instructor, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    booking_date = models.DateTimeField(auto_now_add=True)


