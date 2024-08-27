import csv
import io
from geopy.distance import geodesic
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from rest_framework import status, generics, viewsets, permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from accounts.models import CustomUser
from accounts.serializers import CustomUserSerializer
from .models import InventoryItem, Order, Promotion, ShopperCart, ShopperCartItem, Category
from .serializers import InventoryItemSerializer, OrderSerializer, PromotionSerializer, CartSerializer, CategorySerializer, ProductByCategorySerializer

class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        total_items = InventoryItem.objects.count()
        response_data = {
            'total_items': total_items,
            # Add more summary data as needed
        }
        return Response(response_data)
    
class ProductListView(generics.ListAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]


class IsRetailer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.role == 'retailer'
    


class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsRetailer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
class InventoryItemListView(generics.ListAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
        
class InventoryCreateView(generics.CreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsRetailer]

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

class RetailerListView(generics.ListAPIView):
    queryset = CustomUser.objects.filter(role='retailer')
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.IsAuthenticated]

class InventoryListView(generics.ListAPIView):
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        retailer_id = self.kwargs['retailer_id']
        return InventoryItem.objects.filter(owner_id=retailer_id)

class UploadInventoryView(APIView):
    def post(self, request, *args, **kwargs):
        file = request.FILES.get('file')
        if not file.name.endswith('.csv'):
            return Response({"error": "Only CSV files are supported"}, status=status.HTTP_400_BAD_REQUEST)

        data_set = file.read().decode('UTF-8')
        io_string = io.StringIO(data_set)
        next(io_string)  # Skip the header
        for row in csv.reader(io_string, delimiter=',', quotechar='"'):
            InventoryItem.objects.update_or_create(
                name=row[0],
                description=row[1],
                defaults={
                    'price': row[2],
                    'stock': row[3],
                    'promotion': row[4],
                    'location': row[5],
                    'owner': request.user,
                }
            )

        return Response({"success": "Inventory uploaded successfully"}, status=status.HTTP_201_CREATED)

# Viewset for Inventory Item API
class InventoryItemViewSet(viewsets.ModelViewSet):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer

# Function-based views for inventory operations
def create_inventory(request):
    if request.method == 'POST':
        data = request.POST
        item = InventoryItem.objects.create(
            name=data['name'],
            description=data['description'],
            price=data['price'],
            stock=data['stock'],
            promotion=data.get('promotion', ''),
            location=data['location'],
            owner=request.user,
        )
        return JsonResponse({'success': 'Inventory item created successfully', 'item': InventoryItemSerializer(item).data})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def update_inventory(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id, owner=request.user)
    if request.method == 'POST':
        data = request.POST
        item.name = data['name']
        item.description = data['description']
        item.price = data['price']
        item.stock = data['stock']
        item.promotion = data.get('promotion', '')
        item.location = data['location']
        item.save()
        return JsonResponse({'success': 'Inventory item updated successfully', 'item': InventoryItemSerializer(item).data})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

class InventoryUpdateView(generics.UpdateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

def delete_inventory(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id, owner=request.user)
    if request.method == 'POST':
        item.delete()
        return JsonResponse({'success': 'Inventory item deleted successfully'})
    return JsonResponse({'error': 'Invalid request method'}, status=400)

class InventoryDeleteView(generics.DestroyAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

def view_inventory(request):
    items = InventoryItem.objects.filter(owner=request.user)
    return JsonResponse({'items': InventoryItemSerializer(items, many=True).data})


@api_view(['GET'])
def manage_inventory(request):
    permission_classes = [IsAuthenticated]

    inventory_items = InventoryItem.objects.filter(owner=request.user)
    serializer = InventoryItemSerializer(inventory_items, many=True)
    return Response(serializer.data)

# Promotion views
class PromotionListCreateView(generics.ListCreateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated, IsRetailer]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class PromotionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [permissions.IsAuthenticated, IsRetailer]

    def get_queryset(self):
        return Promotion.objects.filter(owner=self.request.user)
    
@api_view(['GET'])
def manage_promotions(request):
    permission_classes = [IsAuthenticated]

    promotions = Promotion.objects.filter(owner=request.user)
    serializer = PromotionSerializer(promotions, many=True)
    return Response(serializer.data)

# Cart and Order views
class CartView(generics.RetrieveUpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = ShopperCart.objects.get_or_create(user=self.request.user)
        return cart

class OrderListView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class OrderDetailView(generics.RetrieveAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)

class InventoryCartView(generics.RetrieveUpdateAPIView):
    serializer_class = CartSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        cart, created = ShopperCart.objects.get_or_create(user=self.request.user)
        return cart
    

class CategoryListView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    

class ProductsByCategoryView(generics.ListAPIView):
    serializer_class = ProductByCategorySerializer

    def get_queryset(self):
        category_id = self.kwargs['category_id']
        return InventoryItem.objects.filter(category_id=category_id)
