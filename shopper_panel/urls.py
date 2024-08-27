from django.urls import path
from .views import (
    ShopperDashboardView,
    AddToCartView,
    ViewCartView,
)

app_name = 'shopper_panel'

urlpatterns = [
    path('dashboard/', ShopperDashboardView.as_view(), name='shopper_dashboard'),
    path('cart/add/', AddToCartView.as_view(), name='add_to_cart'),
    path('cart/', ViewCartView.as_view(), name='view_cart'),
]
