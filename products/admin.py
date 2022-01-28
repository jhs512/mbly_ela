from django.contrib import admin

# Register your models here.
from products.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    empty_value_display = '-'
    list_display = ('id', 'reg_date', 'update_date', 'market', 'cate_item', 'name', 'display_name')
    list_display_links = tuple(list_display_field for list_display_field in list_display if list_display_field not in [])
    list_filter = ('market', 'cate_item')
    search_fields = ['name', 'display_name']
