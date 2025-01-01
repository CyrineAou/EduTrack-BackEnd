# edu_track/urls.py
from django.urls import path
from api.views import RegisterView, login_view

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', login_view, name='login'),
]
