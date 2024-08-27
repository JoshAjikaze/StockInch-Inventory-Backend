from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from accounts.decorators import admin_required
from accounts.models import CustomUser
from inventory.models import InventoryItem, Category
from .forms import CategoryForm, CustomUserForm, InventoryItemForm, SearchForm 

@login_required
@admin_required
def dashboard_view(request):
    total_users = CustomUser.objects.count()
    total_active_users = CustomUser.objects.filter(is_active=True).count()
    total_retailers = CustomUser.objects.filter(role='retailer').count()
    total_shoppers = CustomUser.objects.filter(role='shopper').count()
    total_products = InventoryItem.objects.count()
    total_categories = Category.objects.count()

    context = {
        'total_users': total_users,
        'total_active_users': total_active_users,
        'total_retailers': total_retailers,
        'total_shoppers': total_shoppers,
        'total_products': total_products,
        'total_categories': total_categories,
    }
    return render(request, 'admin_panel/dashboard.html', context)

@login_required
@admin_required
def categories_view(request):
    categories = Category.objects.all()
    return render(request, 'admin_panel/categories.html', {'categories': categories})

@login_required
@admin_required
def add_category_view(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:categories_view')
    else:
        form = CategoryForm()
    return render(request, 'admin_panel/add_category.html', {'form': form})

@login_required
@admin_required
def edit_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.method == 'POST':
        form = CategoryForm(request.POST, request.FILES, instance=category)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:categories_view')
    else:
        form = CategoryForm(instance=category)
    return render(request, 'admin_panel/edit_category.html', {'form': form})

@login_required
@admin_required
def delete_category_view(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('admin_panel:categories_view')

@login_required
@admin_required
def users_view(request):
    users = CustomUser.objects.all()
    return render(request, 'admin_panel/users.html', {'users': users})

@login_required
@admin_required
def add_user_view(request):
    if request.method == 'POST':
        form = CustomUserForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('admin_panel:users')
    else:
        form = CustomUserForm()
    return render(request, 'admin_panel/add_user.html', {'form': form})


@login_required
@admin_required
def edit_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    if request.method == 'POST':
        form = CustomUserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:users')
    else:
        form = CustomUserForm(instance=user)
    return render(request, 'admin_panel/edit_user.html', {'form': form, 'user': user})


@login_required
@admin_required
def delete_user_view(request, user_id):
    user = get_object_or_404(CustomUser, id=user_id)
    user.delete()
    return redirect('admin_panel:users')

@login_required
@admin_required
def inventory_view(request):
    inventory_items = InventoryItem.objects.select_related('owner', 'category').all()
    return render(request, 'admin_panel/inventory.html', {'inventory_items': inventory_items})

@login_required
@admin_required
def edit_inventory_view(request, item_id):
    inventory_item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES, instance=inventory_item)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:inventory')
    else:
        form = InventoryItemForm(instance=inventory_item)
    return render(request, 'admin_panel/edit_inventory.html', {'form': form})


@login_required
@admin_required
def delete_inventory_view(request, item_id):
    inventory_item = get_object_or_404(InventoryItem, id=item_id)
    if request.method == 'POST':
        inventory_item.delete()
        return redirect('admin_panel:dashboard')
    return render(request, 'admin_panel/delete_inventory.html', {'item': inventory_item})

@login_required
@admin_required
def add_inventory_view(request):
    if request.method == 'POST':
        form = InventoryItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:inventory')
    else:
        form = InventoryItemForm()
    return render(request, 'admin_panel/add_inventory.html', {'form': form})


def search_view(request):
    query = request.GET.get('query')
    users = CustomUser.objects.filter(Q(name__icontains=query) | Q(email__icontains=query))
    inventory_items = InventoryItem.objects.filter(Q(name__icontains=query) | Q(description__icontains=query))
    categories = Category.objects.filter(name__icontains=query)
    context = {
        'users': users,
        'inventory_items': inventory_items,
        'categories': categories,
        'query': query,
    }
    return render(request, 'admin_panel/search_results.html', context)

