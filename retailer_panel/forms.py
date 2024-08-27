from django import forms
from inventory.models import InventoryItem

class InventoryItemForm(forms.ModelForm):
    class Meta:
        model = InventoryItem
        fields = ['name', 'description', 'price', 'image', 'quantity', 'promotion', 'location', 'category']

class UploadInventoryForm(forms.Form):
    file = forms.FileField()
