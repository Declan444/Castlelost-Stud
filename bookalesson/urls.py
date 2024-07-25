from . import views
from django.urls import path

urlpatterns = [
    path('', views.LessonTypesList.as_view(), name='home'),
]