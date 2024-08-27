
from django.db import migrations

def add_default_categories(apps, schema_editor):
    Category = apps.get_model('inventory', 'Category')
    Category.objects.get_or_create(name='Drink')
    Category.objects.get_or_create(name='Food')
    Category.objects.get_or_create(name='Electronics')

class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0005_alter_inventorycart_user_and_more'),
    ]

    operations = [
        migrations.RunPython(add_default_categories),
    ]
