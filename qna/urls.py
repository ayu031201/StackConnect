from django.contrib import admin
from django.urls import path,include
from django.shortcuts import redirect
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.login, name='login'),
    path('feedback/',views.feedback, name='feedback'),
    path('homepage/',include('content.urls')),
]
