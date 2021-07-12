from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('post/<pk>/', views.post_detail, name='post_detail'),
    path('new/', views.create_or_edit_post, name='new_post'),
    path('post/<pk>/edit/', views.create_or_edit_post, name='edit_post'),
]
