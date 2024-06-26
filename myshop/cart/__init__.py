from django.conf import settings

def cart(request):
    cart = request.session.get(settings.CART_SESSION_ID)
    if not cart:
        # Инициализация корзины в сессии, если ее нет
        cart = request.session[settings.CART_SESSION_ID] = {}
    coupon_id = request.session.get('coupon_id')
    return {'cart': cart, 'coupon_id': coupon_id}