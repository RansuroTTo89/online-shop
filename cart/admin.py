from django.contrib import admin
from .models import Cart, CartItem

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['session_id', 'get_total_items', 'get_total', 'created_at']
    search_fields = ['session_id']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart', 'quantity', 'get_cost']
    list_filter = ['cart', 'added_at']
    search_fields = ['product__name']
