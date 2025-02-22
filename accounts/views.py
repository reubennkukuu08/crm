from django.shortcuts import render
from .models import *

# Create your views here.
def home(request):
    customers = Customer.objects.all()
    orders = Order.objects.all()
    total_orders = orders.count()
    orders_deliv = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    context = {
        'customers': customers,
        'orders': orders,
        'total_orders': total_orders,
        'orders_d': orders_deliv,
        'orders_p': orders_pending
    }
    return render(request, 'accounts/dashboard.html', context)

def product(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'accounts/product.html', context)

def customer(request):
    return render(request, 'accounts/customer.html')