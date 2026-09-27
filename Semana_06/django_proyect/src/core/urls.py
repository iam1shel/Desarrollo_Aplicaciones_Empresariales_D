from django.urls import path
from . import views


urlpatterns = [
    path('', views.item_list, name='item_list'),
    path('api/items/', views.item_api, name='item_api'),
]