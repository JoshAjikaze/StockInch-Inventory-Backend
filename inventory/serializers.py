from rest_framework import serializers
from .models import InventoryItem, Category, Order, OrderItem, Promotion, InventoryCart, InventoryCartItem, ShopperCart, ShopperCartItem

class InventoryItemSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'description', 'price', 'stock', 'quantity', 'promotion', 'location', 'category', 'owner', 'image_url']

    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            return request.build_absolute_uri(obj.image.url)
        return None


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = '__all__'

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Promotion
        fields = '__all__'

class InventoryCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryCartItem
        fields = '__all__'

class InventoryCartSerializer(serializers.ModelSerializer):
    items = InventoryCartItemSerializer(many=True, read_only=True)

    class Meta:
        model = InventoryCart
        fields = '__all__'


class CartItemSerializer(serializers.ModelSerializer):
    inventory_item = InventoryItemSerializer()

    class Meta:
        model = ShopperCartItem
        fields = ['id', 'inventory_item', 'quantity']


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True, source='shopper_cart_items')

    class Meta:
        model = ShopperCart
        fields = ['id', 'shopper', 'cart_items']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'icon']

class ProductByCategorySerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = InventoryItem
        fields = ['id', 'name', 'description', 'price', 'stock', 'image', 'category']
