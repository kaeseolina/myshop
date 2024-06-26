from coupons.forms import CouponApplyForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from shop.models import Product
from .cart import Cart
from cart.forms import CartAddProductForm


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(
                            initial={'quantity': item['quantity'],
                            'update': True})
    coupon_apply_form = CouponApplyForm()
    return render(request,
                  'cart/detail.html',
                  {'cart': cart,
                   'coupon_apply_form': coupon_apply_form})
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('cart:cart_detail')

@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
    else:
        cart = None
    return {'cart': cart}

def apply_coupon(request):
    # Реализация применения купона
    pass
def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'shop/product/list.html', {
        'category': category,
        'categories': categories,
        'products': products
    })

@property
def coupon(self):
    if self.coupon_id:
        return Coupon.objects.get(id=self.coupon_id)
    return None

def get_discount(self):
    if self.coupon:
        return (self.coupon.discount / Decimal('100')) * self.get_total_price()
    return Decimal('0')

def get_total_price_after_discount(self):
    return self.get_total_price() - self.get_discount()