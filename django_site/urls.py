from django.urls import path

from django_site.views import catalogue

urlpatterns = [path("", catalogue, name="catalogue")]
