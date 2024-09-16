from . import views
from django.urls import path
from django.views.generic import TemplateView


urlpatterns = [
    path("", TemplateView.as_view(template_name="index.html"), name="home"),
    path("lessons/", views.LessonList.as_view(), name="lessons"),
    path("contact/", views.contact_us, name="contact_us"),
    path(
        "<slug:slug>/edit_comment/<int:comment_id>",
        views.comment_edit,
        name="comment_edit",
    ),
    path(
        "<slug:slug>/delete_comment/<int:comment_id>",
        views.comment_delete,
        name="comment_delete",
    ),
    path("book-a-lesson/", views.book_a_lesson, name="book_a_lesson"),
    path(
        "timeslots/<str:date>/",
        views.timeslots_for_date,
        name="timeslots_for_date",
    ),
    path(
        "booking/<str:date>/<str:slot>/",
        views.booking_form,
        name="booking_form",
    ),
    path("<slug:slug>/", views.lessons_detail, name="lessons_detail"),
]
