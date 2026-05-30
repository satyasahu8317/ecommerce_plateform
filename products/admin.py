# pyrefly: ignore [missing-import]
from django.contrib import admin
from .models import Category, Product, ProductImage
# Register your models here.




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','parent', 'slug']
    list_filter = ['parent']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock','sku', 'in_stock','created','updated']
    list_filter = ['in_stock', 'created', 'updated','category']
    list_editable = ['price', 'stock', 'in_stock']
    prepopulated_fields = {'slug': ('name',)}

    
    