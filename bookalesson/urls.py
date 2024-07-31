from . import views
from django.urls import path
from .views import LessonList


urlpatterns = [
    path('', LessonList.as_view(), name='home'),
    
    path('<slug:slug>/', views.lessons_detail, name='lessons_detail'),
    
]