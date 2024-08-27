from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from inventory.models import Promotion
from inventory.models import InventoryItem
from inventory.serializers import InventoryItemSerializer, PromotionSerializer
from .forms import InventoryItemForm
from accounts.models import CustomUser
from django.db.models import Sum

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
def retailer_dashboard(request):
    if request.user.role != 'retailer' and not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    inventory_items = InventoryItem.objects.filter(owner=request.user)
    data = {
        'inventory_items': list(inventory_items.values())
    }
    return JsonResponse(data, status=200)

class RetailerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != 'retailer':
            return Response({'error': 'Unauthorized'}, status=403)

        total_items = InventoryItem.objects.filter(owner=request.user).count()

        total_inventory_value = InventoryItem.objects.filter(owner=request.user).aggregate(
            total_value=Sum('price')
        )['total_value'] or 0.00

        total_promotions = Promotion.objects.filter(owner=request.user).count()

        response_data = {
            'total_items': total_items,
            'total_inventory_value': total_inventory_value,
            'total_promotions': total_promotions,
            
        }
        return Response(response_data)
    
class InventoryDetailView(generics.RetrieveAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

@login_required
def add_inventory(request):
    if request.user.role != 'retailer' and not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            inventory_item = form.save(commit=False)
            inventory_item.owner = request.user
            inventory_item.save()
            return JsonResponse({'success': 'Inventory item added successfully'}, status=201)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required
def update_inventory(request, item_id):
    if request.user.role != 'retailer' and not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    inventory_item = get_object_or_404(InventoryItem, id=item_id, owner=request.user)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES, instance=inventory_item)
        if form.is_valid():
            form.save()
            return JsonResponse({'success': 'Inventory item updated successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

class InventoryUpdateView(generics.UpdateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

@login_required
def delete_inventory(request, item_id):
    if request.user.role != 'retailer' and not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    inventory_item = get_object_or_404(InventoryItem, id=item_id, owner=request.user)
    if request.method == 'POST':
        inventory_item.delete()
        return JsonResponse({'success': 'Inventory item deleted successfully'}, status=200)
    return JsonResponse({'error': 'Invalid request method'}, status=400)

class InventoryDeleteView(generics.DestroyAPIView):
    queryset = InventoryItem.objects.all()
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

@login_required
def view_inventory(request):
    if request.user.role != 'retailer' and not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    inventory_items = InventoryItem.objects.filter(owner=request.user)
    data = {
        'inventory_items': list(inventory_items.values())
    }
    return JsonResponse(data, status=200)

@login_required
def manage_inventory(request):
    if request.user.role != 'retailer' and not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    inventory_items = InventoryItem.objects.filter(owner=request.user)
    data = {
        'inventory_items': list(inventory_items.values())
    }
    return JsonResponse(data, status=200)

class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return InventoryItem.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class InventoryCreateView(generics.CreateAPIView):
    queryset = InventoryItem.objects.all()
    serializer_class = InventoryItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
        
@login_required
def manage_promotions(request):
    if request.user.role != 'retailer' and not is_admin(request.user):
        return JsonResponse({'error': 'Unauthorized access'}, status=403)
    
    promotions = Promotion.objects.filter(owner=request.user)
    data = {
        'promotions': list(promotions.values())
    }
    return JsonResponse(data, status=200)

class PromotionListCreateView(generics.ListCreateAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        return Promotion.objects.filter(owner=self.request.user)
    

class PromotionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promotion.objects.all()
    serializer_class = PromotionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Promotion.objects.filter(owner=self.request.user)
