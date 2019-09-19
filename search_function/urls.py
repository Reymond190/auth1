from django.contrib import admin
from django.urls import path , include
from django.conf import settings
from django.conf.urls.static import static
from app_auth.views import device_listview,devicelistview
from .views import searchlistview,search_listview



urlpatterns = [
    path('class/<int:pk>/', devicelistview.as_view(), name='class'),
    path('fun/<int:pk>/', device_listview,name='fun'),
    path('one/<int:pk>/',searchlistview,name='ck'),
    path('one/',searchlistview,name='ci'),
    path('one-cbv/',search_listview.as_view(),name='cl'),



]

if settings.DEBUG:
    urlpatterns = urlpatterns+static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)