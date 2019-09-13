from django.urls import path, include
from .views import auto

urlpatterns = [
    path("new/", auto,name='fck')
]