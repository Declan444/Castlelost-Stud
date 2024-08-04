from django.contrib import admin
from .models import Lesson, Instructor, LessonDate, Booking, CommentOnLesson
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Lesson)
class LessonsAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'instructor')
    search_fields = ['title', 'instructor']
    list_filter = ('title', 'instructor')
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content', 'excerpt')
    
@admin.register(LessonDate)
class LessonDateAdmin(admin.ModelAdmin):
    list_display = ('date', 'start_time', 'end_time', 'lesson', 'user')

# Register your models here.
admin.site.register(Instructor)
#admin.site.register(LessonDate)
admin.site.register(Booking)
admin.site.register(CommentOnLesson)