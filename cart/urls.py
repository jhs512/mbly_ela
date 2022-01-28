from django.urls import path

from . import views

app_name = 'cart'

urlpatterns = [
    path('add/', views.add, name='add'),
    path('list/', views.list, name='list'),
    path('delete/<int:cart_item_id>/', views.delete, name='delete'),
    path('modify/<int:cart_item_id>/', views.modify, name='modify'),
    path('delete_items/', views.delete_items, name='delete_items'),
]

