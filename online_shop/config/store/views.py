from django.shortcuts import render, redirect

from store.templatetags.categories import categories
from . import forms
from .forms import RateForm
from .models import *


# Create your views here.


def home(request):
    slides = Slide.objects.all()
    return render(request, 'index.html',{'slides': slides})


def cart(request):
    cart_items = CartItem.objects.filter(customer=request.user)
    total_price = sum([item.total_price() for item in cart_items])
    total_quantity = sum([item.quantity for item in cart_items])

    return render(
        request,
        'cart.html',
        {'cart_items': cart_items, 'total_quantity': total_quantity, 'total_price': total_price}
    )


def delete_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    cart_item.delete()
    return redirect('store:cart')


def edit_cart_item(request, pk):
    cart_item = CartItem.objects.get(pk=pk)
    action = request.GET.get('action')

    if action == 'take' and cart_item.quantity > 0:
        if cart_item.quantity == 1:
            cart_item.delete()
            return redirect('store:cart')
        cart_item.quantity -= 1
        cart_item.save()
        return redirect('store:cart')
    cart_item.quantity += 1
    cart_item.save()
    return redirect('store:cart')


def detail(request, pk):
    product = Products.objects.get(pk=pk)
    return render(request, 'detail.html', {'product': product})


def rate_product(request, pk):
    product = Products.objects.get(pk=pk)
    reviews = Review.objects.filter(product=product)

    if request.method == 'POST':
        form = RateForm(request.POST)
        if form.is_valid():
            rating = form.save(commit=False)
            rating.user = request.user
            rating.product = product
            rating.save()
            return redirect('store:rate_product', pk=pk)
    form = RateForm()
    return render(request, 'rate.html', {'form': form, 'product': product, 'reviews': reviews})


def create_order(request):
    cart_items = CartItem.objects.all()
    total_price = sum([item.total_price() for item in cart_items])
    amount = sum([item.quantity for item in cart_items])
    form = forms.OrderForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        order = Order.objects.create(
            address=request.POST.get('address'),
            phone=request.POST.get('phone'),
            total_price=total_price,
            user=request.user
        )
        for cart_item in cart_items:
            OrderProduct.objects.create(
                order=order,
                product=cart_item.product,
                amount=cart_item.quantity,
                total=cart_item.total_price(),
            )

        cart_items.delete()
        return redirect('store:cart')

    form = forms.OrderForm()
    return render(request, 'order_create.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'amount': amount,
        'form': form})


def orders(request):
    orders_list = Order.objects.filter(user=request.user)
    return render(request, 'orders.html', {'orders': orders_list})


def shop(request):
        category = request.GET.get('category')
        product_id = request.GET.get('product')
        products = Products.objects.all()

        if product_id:
            product = Products.objects.get(pk=product_id)
            cart_item = CartItem.objects.filter(product=product)
            if not cart_item:
                cart_item = CartItem.objects.create(customer=request.user, product=product, quantity=1)
                cart_item.save()
                return redirect('store:shop')
            for item in cart_item:
                item.quantity += 1
                item.save()
            products = products.filter(category=category) if category else products
        return render(request, 'shop.html',{'products': products, categories:'categories'})
