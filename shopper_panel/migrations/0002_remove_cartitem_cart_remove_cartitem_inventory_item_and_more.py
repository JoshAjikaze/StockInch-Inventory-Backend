# Generated by Django 5.0.6 on 2024-08-21 15:33

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_inventorycart_user_and_more'),
        ('shopper_panel', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='inventory_item',
        ),
        migrations.CreateModel(
            name='ShopperCart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_panel_carts', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShopperCartItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_panel_cart_items', to='shopper_panel.shoppercart')),
                ('inventory_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_panel_cart_inventory_items', to='inventory.inventoryitem')),
            ],
        ),
        migrations.AddField(
            model_name='shoppercart',
            name='items',
            field=models.ManyToManyField(through='shopper_panel.ShopperCartItem', to='inventory.inventoryitem'),
        ),
        migrations.CreateModel(
            name='ShopperOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('shopper', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_panel_orders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ShopperOrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField()),
                ('inventory_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_panel_order_inventory_items', to='inventory.inventoryitem')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='shopper_panel_order_items', to='shopper_panel.shopperorder')),
            ],
        ),
        migrations.AddField(
            model_name='shopperorder',
            name='items',
            field=models.ManyToManyField(through='shopper_panel.ShopperOrderItem', to='inventory.inventoryitem'),
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
