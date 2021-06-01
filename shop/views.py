from django.shortcuts import render, get_object_or_404

from .models import Product, Category


def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request, 'shop/home.html', context)


def store(request, category_slug=None):
    categories = None
    products = None

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=categories, is_available=True)
        product_count = products.count()
    else:
        products = Product.objects.all().filter(is_available=True)
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'shop/store.html', context)
