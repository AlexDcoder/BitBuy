from django.contrib import admin

from product.models import Product, Brand, Category

# Register your models here.
admin.site.register([Product, Brand, Category])
