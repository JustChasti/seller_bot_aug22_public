# Generated by Django 4.1 on 2022-08-22 16:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_basket_alter_product_photo_product_tobasket'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Product_toBasket',
            new_name='Product_to_Basket',
        ),
    ]
