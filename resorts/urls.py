from django.urls import path
from . import views

urlpatterns = [
    path('', views.all_resorts, name='resorts'),
    path('<resort_id>', views.resort_detail, name='resort_detail'),
]
