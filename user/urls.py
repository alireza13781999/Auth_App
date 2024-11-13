from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('send-code', views.request_verification, name='request_verification'),
    path('verify-code', views.verify_code, name='verify_code'),
    path('register', views.complete_registration, name='complete_registration'),
    path('login', views.login, name='login'),
]
