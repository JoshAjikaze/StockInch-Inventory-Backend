from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static



urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin_tools/', include('admin_tools.urls')),
     path('admin-panel/', include('admin_panel.urls', namespace='admin_panel')),
    path('accounts/', include('accounts.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('inventory/', include('inventory.urls', namespace='inventory')),
    path('retailer-panel/', include('retailer_panel.urls')),
    path('shopper-panel/', include('shopper_panel.urls')),
    path('api/admin/', include('admin_panel.urls')),
    path('api/retailer/', include('retailer_panel.urls')),
    path('api/shopper/', include('shopper_panel.urls')),
    path('api/inventory/', include('inventory.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
