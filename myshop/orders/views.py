from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreateForm
from cart.cart import Cart
from django.core.mail import send_mail
from .tasks import order_created
import logging


logger = logging.getLogger(__name__)

def send_order_email(order):
    try:
        subject = f'Order nr. {order.id}'
        message = f'Dear {order.first_name},\n\nYou have successfully placed an order. Your order ID is {order.id}.'
        send_mail(subject, message, 'your-email@example.com', [order.email])
        logger.debug('Email sent successfully to %s', order.email)
    except Exception as e:
        logger.error(f'Error sending order email: {e}')

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Clear the cart
            cart.clear()
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})


def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                         product=item['product'],
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Clear the cart
            cart.clear()

            # Отправка письма с информацией о заказе
            send_order_email(order)

            # запуск асинхронной задачи
            order_created.delay(order.id)
            return render(request, 'orders/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'orders/order/create.html', {'cart': cart, 'form': form})





def admin_order_detail(request):
    return None