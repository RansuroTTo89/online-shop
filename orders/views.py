from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from cart.models import Cart
from cart.views import get_or_create_cart
from .models import Order, OrderItem
import uuid

@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    
    if not cart.items.exists():
        messages.error(request, 'Your cart is empty')
        return redirect('cart:cart')
    
    if request.method == 'POST':
        order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        
        order = Order.objects.create(
            user=request.user,
            cart=cart,
            order_number=order_number,
            first_name=request.POST.get('first_name'),
            last_name=request.POST.get('last_name'),
            email=request.POST.get('email'),
            phone=request.POST.get('phone'),
            address=request.POST.get('address'),
            city=request.POST.get('city'),
            state=request.POST.get('state'),
            zip_code=request.POST.get('zip_code'),
            total_amount=cart.get_total(),
        )
        
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price,
            )
        
        cart.items.all().delete()
        messages.success(request, 'Order placed successfully!')
        return redirect('orders:order_detail', order_id=order.id)
    
    context = {
        'cart': cart,
        'cart_items': cart.items.all(),
        'total': cart.get_total(),
    }
    return render(request, 'orders/checkout.html', context)

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    if order.user != request.user and not request.user.is_staff:
        messages.error(request, 'You do not have permission to view this order')
        return redirect('shop:home')
    
    context = {
        'order': order,
        'order_items': order.items.all(),
    }
    return render(request, 'orders/order_detail.html', context)

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'orders': orders,
    }
    return render(request, 'orders/order_list.html', context)
