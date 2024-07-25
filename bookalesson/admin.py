from django.contrib import admin
from .models import LessonType, Instructor, LessonDate, BookingDate

# Register your models here.
admin.site.register(LessonType)
admin.site.register(Instructor)
admin.site.register(LessonDate)
admin.site.register(BookingDate)