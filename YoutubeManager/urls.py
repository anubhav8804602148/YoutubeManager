from .views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("", showHomePage),
    path("downloadVideo", downloadVideo)
]
