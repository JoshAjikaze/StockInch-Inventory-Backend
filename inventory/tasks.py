from celery import shared_task
from django.core.mail import send_mail
from .models import InventoryItem

@shared_task
def check_inventory_levels():
    low_inventory_items = InventoryItem.objects.filter(quantity__lt=5)
    for item in low_inventory_items:
        send_mail(
            'Low Inventory Alert',
            f'The item {item.name} is low on stock. Only {item.quantity} left.',
            'from@example.com',
            [item.owner.email],
        )
