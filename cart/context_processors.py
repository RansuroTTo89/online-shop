from .models import Cart

def cart_context(request):
    try:
        session_id = request.session.session_key
        if session_id:
            cart = Cart.objects.get(session_id=session_id)
            return {
                'cart_items_count': cart.get_total_items(),
                'cart_total': cart.get_total(),
            }
    except Cart.DoesNotExist:
        pass
    
    return {
        'cart_items_count': 0,
        'cart_total': 0,
    }
