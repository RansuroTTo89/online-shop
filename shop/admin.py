from django.contrib import admin
from .models import Category, Product, Review

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock', 'is_active', 'created_at']
    list_filter = ['category', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {'fields': ('name', 'slug', 'category')}),
        ('Details', {'fields': ('description', 'price', 'stock')}),
        ('Media', {'fields': ('image',)}),
        ('Status', {'fields': ('is_active',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'author', 'rating', 'created_at']
    list_filter = ['rating', 'created_at', 'product']
    search_fields = ['title', 'content', 'product__name']
    readonly_fields = ['created_at', 'updated_at']
