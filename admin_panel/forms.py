from django import forms
from inventory.models import Category
from accounts.models import CustomUser
from inventory.models import InventoryItem


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'icon']
        

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'name', 'phone_number', 'role']
        

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'description', 'price', 'image', 'stock', 'promotion', 'location', 'category']
        
class SearchForm(forms.Form):
    query = forms.CharField(label='Search', max_length=100)
