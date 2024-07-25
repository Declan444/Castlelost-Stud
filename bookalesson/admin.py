from django.contrib import admin
from .models import Lessons, Instructor, LessonDate, Bookings, CommentOnLesson

# Register your models here.
admin.site.register(Lessons)
admin.site.register(Instructor)
admin.site.register(LessonDate)
admin.site.register(Bookings)
admin.site.register(CommentOnLesson)