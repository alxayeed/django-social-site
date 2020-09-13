from django.urls import path
from . import views

app_name = 'images'
urlpatterns = [
    path('create/', views.create_image, name='create'),
    path('detail/<int:id>/<slug:slug>/',
         views.image_detail, name='detail'),
    path('like/', views.like_image, name='like'),
    path('', views.image_list, name='list'),

]
