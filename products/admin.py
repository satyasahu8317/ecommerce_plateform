# pyrefly: ignore [missing-import]
from django.contrib import admin
from .models import Category, Product, ProductImage, Attribute, AttributeValue, ProductVariant, Review
# Register your models here.

admin.site.register(Attribute)
admin.site.register(AttributeValue)
admin.site.register(Review)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name','parent', 'slug']
    list_filter = ['parent']
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock','sku', 'in_stock','created','updated']
    list_filter = ['in_stock', 'created', 'updated','category']
    list_editable = ['price', 'stock', 'in_stock']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]

    
