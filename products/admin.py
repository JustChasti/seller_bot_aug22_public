from django.contrib import admin
from products.models import Product, Basket, Product_to_Basket

# Register your models here.

admin.site.register(Product)
admin.site.register(Basket)
admin.site.register(Product_to_Basket)
