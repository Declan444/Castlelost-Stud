from django.contrib import admin
from .models import Lesson, Instructor, LessonDate, Booking, CommentOnLesson
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Lesson)
class LessonsAdmin(SummernoteModelAdmin):
    list_display = ("title", "slug", "instructor")
    search_fields = ["title", "instructor"]
    list_filter = ("title", "instructor")
    prepopulated_fields = {"slug": ("title",)}
    summernote_fields = ("content", "excerpt")


@admin.register(LessonDate)
class LessonDateAdmin(admin.ModelAdmin):
    list_display = ("date", "start_time", "end_time", "lesson", "user")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "lesson_date",
        "lesson_type",
        "instructor",
        "status",
        "booking_date",
    )
    list_filter = ("status", "lesson_date", "lesson_type", "instructor")
    search_fields = (
        "user__username",
        "lesson_type__title",
        "instructor__name",
    )


@admin.register(CommentOnLesson)
class CommentOnLessonAdmin(admin.ModelAdmin):
    list_display = (
        "author",
        "lesson_type",
        "lesson_date",
        "text",
        "created_on",
        "approved",
    )
    list_filter = ("created_on", "approved", "lesson_type", "lesson_date")


admin.site.register(Instructor)
