from django.urls import path
from .views import (
    RetailerDashboardView, InventoryListCreateView, InventoryDetailView,
    InventoryCreateView, InventoryUpdateView, InventoryDeleteView,
    PromotionListCreateView, PromotionDetailView
)

app_name = 'retailer_panel'

urlpatterns = [
    path('dashboard/', RetailerDashboardView.as_view(), name='retailer_dashboard'),
    path('inventory/', InventoryListCreateView.as_view(), name='inventory_list_create'),
    path('inventory/add/', InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory_detail'),
    path('inventory/update/<int:pk>/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/delete/<int:pk>/', InventoryDeleteView.as_view(), name='inventory_delete'),
    path('promotions/', PromotionListCreateView.as_view(), name='promotion_list_create'),
    path('promotions/<int:pk>/', PromotionDetailView.as_view(), name='promotion_detail'),
]
