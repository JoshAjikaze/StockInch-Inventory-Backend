from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='user_signup'),
    path('login/', views.login_view, name='user_login'),
    path('set_preference/', views.set_preference, name='set_preference'),
    path('home/', views.home, name='user_home'),
    path('search/', views.search_item, name='search_item'),
    path('item/<int:item_id>/', views.view_item, name='view_item'),
    path('grocery_list/', views.grocery_list, name='grocery_list'),
    path('map/', views.real_time_map, name='real_time_map'),
]
