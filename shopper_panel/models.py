from django.db import models
from accounts.models import CustomUser
from inventory.models import InventoryItem

class ShopperCart(models.Model):
    shopper = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart_items = models.ManyToManyField(InventoryItem, through='ShopperCartItem', related_name='shopper_cart_items')


class ShopperCartItem(models.Model):
    cart = models.ForeignKey(ShopperCart, on_delete=models.CASCADE, related_name='shopper_panel_cart_items')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='shopper_panel_cart_inventory_items')
    quantity = models.PositiveIntegerField(default=1)

class ShopperOrder(models.Model):
    shopper = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shopper_panel_orders')
    items = models.ManyToManyField(InventoryItem, through='ShopperOrderItem')
    created_at = models.DateTimeField(auto_now_add=True)

class ShopperOrderItem(models.Model):
    order = models.ForeignKey(ShopperOrder, on_delete=models.CASCADE, related_name='shopper_panel_order_items')
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='shopper_panel_order_inventory_items')
    quantity = models.PositiveIntegerField()
