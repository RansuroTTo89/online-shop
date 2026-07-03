from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from shop.models import Product
from .models import Cart, CartItem

def get_or_create_cart(request):
    session_id = request.session.session_key
    if not session_id:
        request.session.create()
        session_id = request.session.session_key
    
    cart, created = Cart.objects.get_or_create(session_id=session_id)
    return cart

def cart_view(request):
    cart = get_or_create_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total': cart.get_total(),
        'total_items': cart.get_total_items(),
    }
    return render(request, 'cart/cart.html', context)

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    cart = get_or_create_cart(request)
    
    quantity = int(request.POST.get('quantity', 1))
    
    if product.stock < quantity:
        messages.error(request, 'Not enough stock available')
        return redirect('shop:product', slug=slug)
    
    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product,
        defaults={'quantity': quantity}
    )
    
    if not created:
        cart_item.quantity += quantity
        if cart_item.quantity > product.stock:
            cart_item.quantity = product.stock
            messages.warning(request, 'Limited to available stock')
        cart_item.save()
    
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:cart')

def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    
    if request.method == 'POST':
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity <= 0:
            cart_item.delete()
            messages.success(request, 'Item removed from cart')
        elif quantity > cart_item.product.stock:
            messages.error(request, 'Not enough stock')
        else:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated')
    
    return redirect('cart:cart')

def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('cart:cart')

def clear_cart(request):
    cart = get_or_create_cart(request)
    cart.items.all().delete()
    messages.success(request, 'Cart cleared')
    return redirect('cart:cart')
