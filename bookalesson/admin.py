from django.contrib import admin
from .models import Lessons, Instructor, LessonDate, Bookings, CommentOnLesson
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Lessons)
class LessonsAdmin(SummernoteModelAdmin):

    list_display = ('title', 'slug', 'instructor')
    search_fields = ['title']
    list_filter = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    summernote_fields = ('content', 'excerpt')

# Register your models here.
admin.site.register(Instructor)
admin.site.register(LessonDate)
admin.site.register(Bookings)
admin.site.register(CommentOnLesson)