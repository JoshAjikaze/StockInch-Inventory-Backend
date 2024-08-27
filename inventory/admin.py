from django.contrib import admin
from .models import InventoryItem, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'price', 'location', 'owner', 'category')
    list_filter = ('location', 'owner', 'category')
    search_fields = ('name', 'description')
    ordering = ('name',)




