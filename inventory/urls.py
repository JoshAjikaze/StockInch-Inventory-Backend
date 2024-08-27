from django.urls import path
from .views import (
    InventoryCartView, InventoryListCreateView, InventoryListView, InventoryDetailView, InventoryCreateView, 
    InventoryUpdateView, InventoryDeleteView, InventoryItemViewSet, DashboardView, OrderDetailView, OrderListView, ProductListView, PromotionDetailView, PromotionListCreateView, RetailerListView, 
    UploadInventoryView, create_inventory, update_inventory, 
    delete_inventory, view_inventory, manage_inventory, manage_promotions,  CategoryListView,
    ProductsByCategoryView
)
from rest_framework.routers import DefaultRouter

app_name = 'inventory'

router = DefaultRouter()
router.register(r'inventory', InventoryItemViewSet, basename='inventoryitem')

urlpatterns = router.urls

urlpatterns += [
    path('upload-inventory/', UploadInventoryView.as_view(), name='upload_inventory'),
    path('item/new/', InventoryCreateView.as_view(), name='inventory_create'),
    path('item/<int:pk>/edit/', InventoryUpdateView.as_view(), name='inventory_edit'),
    path('item/<int:pk>/delete/', InventoryDeleteView.as_view(), name='inventory_delete'),
    path('', InventoryListView.as_view(), name='inventory_list'),
    path('item/<int:pk>/', InventoryDetailView.as_view(), name='inventory_detail'),
    path('create/', create_inventory, name='create_inventory'),
    path('update/<int:item_id>/', update_inventory, name='update_inventory'),
    path('delete/<int:item_id>/', delete_inventory, name='delete_inventory'),
    path('view/', view_inventory, name='view_inventory'),
    path('manage/', manage_inventory, name='manage_inventory'),
    path('manage/promotions/', manage_promotions, name='manage_promotions'),
    path('api/inventory/', InventoryListCreateView.as_view(), name='inventory_list_create'),
    path('api/inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory_detail'),
    path('api/dashboard/', DashboardView.as_view(), name='dashboard'),
    path('api/retailers/', RetailerListView.as_view(), name='retailer_list'),
    path('api/retailers/<int:retailer_id>/inventory/', InventoryListView.as_view(), name='retailer_inventory_list'),
    #path('api/distance/', DistanceView.as_view(), name='distance'),
    path('api/promotions/', PromotionListCreateView.as_view(), name='promotion_list_create'),
    path('api/promotions/<int:pk>/', PromotionDetailView.as_view(), name='promotion_detail'),
    path('api/cart/', InventoryCartView.as_view(), name='cart'),
    path('api/orders/', OrderListView.as_view(), name='order_list'),
    path('api/orders/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    path('products/', ProductListView.as_view(), name='product_list'),
    path('categories/', CategoryListView.as_view(), name='category_list'),
    path('categories/<int:category_id>/products/', ProductsByCategoryView.as_view(), name='products_by_category'),
]
