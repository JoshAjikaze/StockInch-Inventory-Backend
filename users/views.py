from django.shortcuts import render, redirect
from inventory.models import InventoryItem


def signup(request):
    # Signup logic here
    return render(request, 'user/signup.html')

def login_view(request):
    # Login logic here
    return render(request, 'user/login.html')

def set_preference(request):
    # Set preference logic here
    return render(request, 'user/set_preference.html')

def home(request):
    # Home screen logic here
    return render(request, 'user/home.html')

def search_item(request):
    # Search item logic here
    return render(request, 'user/search.html')

def view_item(request, item_id):
    # View item details logic here
    return render(request, 'user/view_item.html')

def grocery_list(request):
    # Grocery list management logic here
    return render(request, 'user/grocery_list.html')

def real_time_map(request):
    # Real-time map logic here
    return render(request, 'user/real_time_map.html')

def search_item(request):
    query = request.GET.get('query', '')
    items = InventoryItem.objects.filter(name__icontains=query)
    return render(request, 'user/search.html', {'items': items})

def view_item(request, item_id):
    item = InventoryItem.objects.get(id=item_id)
    return render(request, 'user/view_item.html', {'item': item})
