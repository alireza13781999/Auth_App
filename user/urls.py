from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('send-code', views.send_code, name='send-code'),
    path('verify-code', views.verify_code, name='verify_code'),
    path('register', views.register, name='register'),
    path('login', views.login, name='login'),
]
