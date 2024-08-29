from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from inventory.models import InventoryItem
from inventory.serializers import CartItemSerializer 
from .models import ShopperCart, ShopperCartItem
from .forms import AddToCartForm
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def shopper_dashboard(request):
    if request.user.role != 'shopper' and not is_admin(request.user):
        return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
    return Response({"message": "Welcome to the Shopper Dashboard"}, status=status.HTTP_200_OK)

class ShopperDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        cart_items = ShopperCart.objects.filter(shopper=request.user).count()
        inventory_items = InventoryItem.objects.filter(stock__gt=0).count()

        response_data = {
            'cart_items': cart_items,
            'inventory_items': inventory_items,
           
        }

        return Response(response_data)

@login_required
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_to_cart(request):
    if request.user.role != 'shopper' and not is_admin(request.user):
        return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
    form = AddToCartForm(request.data)
    if form.is_valid():
        cart_item = form.save(commit=False)
        cart, created = ShopperCart.objects.get_or_create(shopper=request.user)
        cart_item.cart = cart
        cart_item.save()
        return Response({"message": "Item added to cart successfully"}, status=status.HTTP_201_CREATED)
    return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

class AddToCartView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        inventory_item_id = request.data.get('inventory_item_id')
        quantity = request.data.get('quantity', 1)

        try:
            inventory_item = InventoryItem.objects.get(id=inventory_item_id)
        except InventoryItem.DoesNotExist:
            return Response({"error": "Inventory item not found."}, status=status.HTTP_404_NOT_FOUND)

        cart, created = ShopperCart.objects.get_or_create(shopper=request.user)
        cart_item, created = ShopperCartItem.objects.get_or_create(cart=cart, item=inventory_item)
        cart_item.quantity += quantity
        cart_item.save()

        return Response({"success": "Item added to cart."}, status=status.HTTP_200_OK)

@login_required
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def view_cart(request):
    if request.user.role != 'shopper' and not is_admin(request.user):
        return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)
    cart = get_object_or_404(ShopperCart, shopper=request.user)
    cart_items = ShopperCartItem.objects.filter(cart=cart)
    cart_items_data = [
        {
            "item_id": item.id,
            "item_name": item.inventory_item.name,
            "quantity": item.quantity
        }
        for item in cart_items
    ]
    return Response({"cart_items": cart_items_data}, status=status.HTTP_200_OK)

class ViewCartView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            cart = ShopperCart.objects.get(shopper=request.user)
        except ShopperCart.DoesNotExist:
            return Response({"error": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

        cart_items = ShopperCartItem.objects.filter(cart=cart)
        serializer = CartItemSerializer(cart_items, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
