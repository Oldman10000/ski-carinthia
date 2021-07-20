from django.urls import path
from . import views

urlpatterns = [
    path('', views.blogs, name='blogs'),
    path('post/<pk>/', views.post_detail, name='post_detail'),
    path('new/', views.create_or_edit_post, name='new_post'),
    path('post/<pk>/edit/', views.create_or_edit_post, name='edit_post'),
    path('post/<pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<postpk>/<pk>/addpoint/', views.add_point, name='add_point'),
    path('post/<postpk>/<pk>/deletepoint/', views.delete_point, name='delete_point'),
]
