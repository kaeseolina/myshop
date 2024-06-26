from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.db.models import Count



def category_view(request, category_name):
    category = get_object_or_404(Category, name=category_name)
    products = Product.objects.filter(category=category)
    return render(request, 'shop/category.html', {'category': category, 'products': products})

def category_view(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category)
    categories = Category.objects.all()

    return render(request, 'shop/category.html', {
        'category': category,
        'products': products,
        'categories': categories,
    })
def product_list_by_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    products = Product.objects.filter(category=category, available=True)
    return render(request, 'shop/product/list.html', {'category': category, 'products': products})


def product_list(request, category_slug=None):
    category = None
    products = Product.objects.filter(available=True)

    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # Фильтрация категорий, которые имеют доступные продукты
    categories = Category.objects.filter(products__available=True).distinct()

    context = {
        'category': category,
        'categories': categories,
        'products': products
    }
    return render(request, 'shop/product/list.html', context)


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm()

    # Получаем следующий и предыдущий продукт
    next_product = Product.objects.filter(category=product.category, id__gt=product.id, available=True).order_by(
        'id').first()
    previous_product = Product.objects.filter(category=product.category, id__lt=product.id, available=True).order_by(
        '-id').first()

    return render(request, 'shop/product/detail.html', {
        'product': product,
        'cart_product_form': cart_product_form,
        'next_product': next_product,
        'previous_product': previous_product,
    })

def set_session(request):
    request.session['foo'] = 'bar'
    return HttpResponse('Значение "bar" установлено для ключа "foo" в сессии.')

def get_session(request):
    foo_value = request.session.get('foo')
    if foo_value is not None:
        return HttpResponse(f'Значение ключа "foo" в сессии: {foo_value}')
    else:
        return HttpResponse('Ключ "foo" отсутствует в сессии или его значение None.')

def delete_session(request):
    if 'foo' in request.session:
        del request.session['foo']
        return HttpResponse('Ключ "foo" успешно удален из сессии.')
    else:
        return HttpResponse('Ключ "foo" отсутствует в сессии.')
