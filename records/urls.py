from django.conf.urls import url
from django.urls import path
from django.contrib import admin
from django.urls.resolvers import URLPattern
from records import views
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('', views.upload_file_view, name="index"),
]