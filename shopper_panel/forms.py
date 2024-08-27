from django import forms
from .models import ShopperCartItem

class AddToCartForm(forms.ModelForm):
    class Meta:
        model = ShopperCartItem
        fields = ['inventory_item', 'quantity']
