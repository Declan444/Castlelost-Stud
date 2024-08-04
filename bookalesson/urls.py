from . import views
from django.urls import path
from django.views.generic import TemplateView
from .views import LessonList, lessons_detail


urlpatterns = [
    path('book-a-lesson/', TemplateView.as_view(template_name='book_a_lesson.html'), name='book_a_lesson'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('lessons/', LessonList.as_view(), name='lessons'),   
    path('<slug:slug>/', lessons_detail, name='lessons_detail'),
     
    
]