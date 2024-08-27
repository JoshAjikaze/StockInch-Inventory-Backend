from django.urls import path
from . import views

app_name = 'retailer_panel'

urlpatterns = [
    path('dashboard/', views.RetailerDashboardView.as_view(), name='retailer_dashboard'),
    path('inventory/', views.InventoryListCreateView.as_view(), name='inventory_list_create'),
    path('inventory/add/', views.InventoryCreateView.as_view(), name='add_inventory'),
    path('inventory/update/<int:pk>/', views.InventoryUpdateView.as_view(), name='update_inventory'),
    path('inventory/delete/<int:pk>/', views.InventoryDeleteView.as_view(), name='delete_inventory'),
    path('inventory/detail/<int:pk>/', views.InventoryDetailView.as_view(), name='inventory_detail'),
    path('promotions/', views.PromotionListCreateView.as_view(), name='promotion_list_create'),
    path('promotions/<int:pk>/', views.PromotionDetailView.as_view(), name='promotion_detail'),
]
