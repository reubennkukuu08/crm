from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import *
from django.contrib.auth.models import Group

# Create your views here.
@authenticated_users
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='customer')
            user.groups.add(group)

            # Create the Customer
            Customer.objects.create(user=user,
                name=f"{form.cleaned_data.get('first_name')} {form.cleaned_data.get('last_name')}",
                phone=form.cleaned_data.get('phone'),
                email=form.cleaned_data.get('email'))

            messages.success(request, f'Account was successfully created for {username}')
            return redirect('login')
    context = {'form': form}
    return render(request, 'accounts/register.html', context)

@authenticated_users
def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR Password is incorrect!')
    return render(request, 'accounts/login.html')


def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
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


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product(request):
    products = Product.objects.all()
    context = {
        'products' : products
    }
    return render(request, 'accounts/product.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk):
    customer = Customer.objects.get(id=pk)
    orders = customer.order_set.all()
    total_orders = customer.order_set.all().count()

    context = {
        'customer' : customer,
        'orders': orders,
        'total_orders': total_orders,
    }
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    orders_deliv = orders.filter(status='Delivered').count()
    orders_pending = orders.filter(status='Pending').count()
    context = {
        'orders': orders,
        'total_orders': total_orders,
        'orders_d': orders_deliv,
        'orders_p': orders_pending
    }
    return render(request, 'accounts/user.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def create_order(request, pk):
    customer = Customer.objects.get(id=pk)
    form = OrderForm(initial={'customer': customer})
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
       'form': form
    }

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def update_order(request, pk):
    print(f"Received pk: {pk} (Type: {type(pk)})")
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {
       'form': form
    }

    return render(request, 'accounts/order_form.html', context)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def delete_order(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    context = {
        'item': order
    }
    return render(request, 'accounts/delete.html', context)