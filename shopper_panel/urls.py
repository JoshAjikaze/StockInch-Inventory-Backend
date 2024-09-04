from django.urls import path
from .views import (
   ShopperDashboardView, ShopperEditProfileView, add_to_cart, remove_from_cart, view_cart, ProductDetailView, RetailerProductListView
)

app_name = 'shopper_panel'

urlpatterns = [
    path('dashboard/', ShopperDashboardView.as_view(), name='shopper_dashboard'),
    path('profile/edit/', ShopperEditProfileView.as_view(), name='shopper_edit_profile'),
    path('cart/add/', add_to_cart, name='add_to_cart'),
    path('cart/remove/', remove_from_cart, name='remove_from_cart'),
    path('cart/', view_cart, name='view_cart'),
    path('products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
    path('retailer/<int:retailer_id>/products/', RetailerProductListView.as_view(), name='retailer_product_list'),
]
