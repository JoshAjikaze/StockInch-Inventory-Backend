from django.shortcuts import get_object_or_404
from inventory.models import InventoryItem
from inventory.serializers import CartItemSerializer, InventoryItemSerializer
from .models import ShopperCart, ShopperCartItem
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status, generics

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'


class ShopperDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart_items = ShopperCartItem.objects.filter(cart__shopper=request.user).count() 
        inventory_items = InventoryItem.objects.filter(stock__gt=0).count()

        response_data = {
            'cart_items': cart_items,
            'inventory_items': inventory_items,
        }

        return Response(response_data, status=status.HTTP_200_OK)

class ShopperEditProfileView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    inventory_item_id = request.data.get('inventory_item_id')
    quantity = request.data.get('quantity', 1)

    try:
        inventory_item = InventoryItem.objects.get(id=inventory_item_id)
    except InventoryItem.DoesNotExist:
        return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)

    cart, created = ShopperCart.objects.get_or_create(shopper=request.user)
    cart_item, created = ShopperCartItem.objects.get_or_create(cart=cart, inventory_item=inventory_item)
    cart_item.quantity = int(quantity)
    cart_item.save()

    return Response({"success": "Item added to cart."}, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def remove_from_cart(request):
    inventory_item_id = request.data.get('inventory_item_id')

    try:
        inventory_item = InventoryItem.objects.get(id=inventory_item_id)
    except InventoryItem.DoesNotExist:
        return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)

    cart = get_object_or_404(ShopperCart, shopper=request.user)
    cart_item = get_object_or_404(ShopperCartItem, cart=cart, inventory_item=inventory_item)
    cart_item.delete()

    return Response({"success": "Item removed from cart."}, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    cart = get_object_or_404(ShopperCart, shopper=request.user)
    cart_items = ShopperCartItem.objects.filter(cart=cart)
    serializer = CartItemSerializer(cart_items, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            product = InventoryItem.objects.get(pk=pk)
        except InventoryItem.DoesNotExist:
            return Response({"error": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = InventoryItemSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RetailerProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, retailer_id):
        products = InventoryItem.objects.filter(owner_id=retailer_id)
        serializer = InventoryItemSerializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

