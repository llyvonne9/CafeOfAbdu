from django.urls import path, include
from . import views


urlpatterns = [
    path('create', views.create,name='create'),
    path('<int:restaurant_id>', views.detail,name='detail'),
    path('<int:restaurant_id>/like', views.like,name='like'),
    path('<int:restaurant_id>/delete', views.delete,name='delete'),
    path('<int:restaurant_id>/add_dish', views.add_dish,name='add_dish'),
    path('<int:restaurant_id>/<int:serve_id>/like_dish', views.like_dish,name='like_dish'),

]
