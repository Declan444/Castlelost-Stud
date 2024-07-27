from . import views
from django.urls import path

urlpatterns = [
    path('', views.LessonTypesList.as_view(), name='home'),
    path('<slug:slug>/', views.lessons_detail, name='lessons_detail'),
    
]