from django.db import models
from accounts.models import CustomUser

class Category(models.Model):
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='category_icons/')

    def __str__(self):
        return self.name

class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    image = models.ImageField(upload_to='inventory_images/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    quantity = models.PositiveIntegerField(default=0)
    promotion = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=255)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inventory_items', null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='items')

    def __str__(self):
        return self.name

class Promotion(models.Model):
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='promotions')
    name = models.CharField(max_length=255)
    description = models.TextField()
    discount = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()

class InventoryCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inventory_carts')
    items = models.ManyToManyField(InventoryItem, through='InventoryCartItem')

class InventoryCartItem(models.Model):
    cart = models.ForeignKey(InventoryCart, on_delete=models.CASCADE, related_name='inventory_cart_items_set')
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='inventory_cart_items_inventory')
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='inventory_orders')
    items = models.ManyToManyField(InventoryItem, through='OrderItem')
    created_at = models.DateTimeField(auto_now_add=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='inventory_order_items_set')
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='inventory_order_items_inventory')
    quantity = models.PositiveIntegerField()

class ShopperCart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='shopper_inventory_carts')
    items = models.ManyToManyField(InventoryItem, through='ShopperCartItem', related_name='shopper_inventory_cart_items')

    def __str__(self):
        return f"Cart of {self.user.email}"

class ShopperCartItem(models.Model):
    cart = models.ForeignKey(ShopperCart, on_delete=models.CASCADE, related_name='shopper_inventory_cart_items_set')
    item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE, related_name='shopper_inventory_cart_items_inventory')
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name} in cart"
