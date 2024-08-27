from . import views
from django.urls import path
from .views import (
    dashboard_view,
    categories_view,
    add_category_view,
    edit_category_view,
    delete_category_view,
    users_view,
    inventory_view, 
    edit_user_view,
    delete_user_view, 
    edit_inventory_view, 
    delete_inventory_view,
    add_inventory_view
)


app_name = 'admin_panel'

urlpatterns = [
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('categories/', views.categories_view, name='categories_view'),
    path('categories/add/', views.add_category_view, name='add_category'),
    path('categories/edit/<int:category_id>/', views.edit_category_view, name='edit_category'), 
    path('categories/delete/<int:category_id>/', views.delete_category_view, name='delete_category'),
    path('users/', views.users_view, name='users'),
    path('users/add/', views.add_user_view, name='add_user'),
    path('users/edit/<int:user_id>/', views.edit_user_view, name='edit_user'),
    path('users/delete/<int:user_id>/', views.delete_user_view, name='delete_user'),
    path('inventory/', inventory_view, name='inventory_view'),
    path('inventory/edit/<int:item_id>/', edit_inventory_view, name='edit_inventory'),
    path('inventory/delete/<int:item_id>/', delete_inventory_view, name='delete_inventory'),
    path('inventory/add/', add_inventory_view, name='add_inventory'),
    path('search/', views.search_view, name='search'),
]
