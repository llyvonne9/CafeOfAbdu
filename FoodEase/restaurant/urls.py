from django.urls import path, include
from . import views


urlpatterns = [
    path('create', views.create,name='create'),
    path('<int:restaurant_id>', views.detail,name='detail'),
    path('<int:restaurant_id>/like', views.like,name='like'),
    path('<int:restaurant_id>/delete', views.delete,name='delete'),

]
