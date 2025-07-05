from django.contrib import admin
from django.urls import path
from.import views
from app.views import index

app_name = "app"
urlpatterns = [
    path('', index, name="index"),
]