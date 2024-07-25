from django.contrib import admin
from .models import LessonType, Instructor

# Register your models here.
admin.site.register(LessonType)
admin.site.register(Instructor)