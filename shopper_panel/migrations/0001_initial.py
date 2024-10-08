# Generated by Django 5.0.6 on 2024-08-01 21:16

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('inventory', '0004_rename_cartitem_inventorycartitem_inventorycart_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_carts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_cart_items', to='shopper_panel.cart')),
                ('inventory_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_cart_items', to='inventory.inventoryitem')),
            ],
        ),
        migrations.AddField(
            model_name='cart',
            name='items',
            field=models.ManyToManyField(through='shopper_panel.CartItem', to='inventory.inventoryitem'),
        ),
    ]
