from django.shortcuts import render

from .models import Product, Category


def home(request):
    products = Product.objects.all().filter(is_available=True)

    context = {
        'products': products,
    }
    return render(request, 'shop/home.html', context)


def store(request):
    products = Product.objects.all().filter(is_available=True)
    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count
    }
    return render(request, 'shop/store.html', context)
