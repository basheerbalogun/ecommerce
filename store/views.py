from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404

from .models import Category, Product, Cart, CartItem
from .forms import CreateProductForm


def home(request):
    q = request.GET.get('q') if request.GET.get("q") is not None else ""
    categories = Category.objects.all()
    cart_num = Cart.objects.all().count()
    products = Product.objects.filter(Q(name__icontains=q)
                                      | Q(category__name__icontains=q)
                                      | Q(small_description__icontains=q)).order_by('create_at'
                                                                                    ).exclude(status=True)
    num_category = Category.objects.all().count()
    context = {
        'categories': categories,
        'products': products,
        'num_category': num_category,
        'cart_num': cart_num
    }
    return render(request, 'store/home.html', context)


def category_detail(request, slug):
    category_detail = Category.active_object.filter(slug=slug)
    context = {
        'category_detail': category_detail
    }
    return render(request, 'store/category-detail.html', context)


def question_answer(request):
    return render(request, 'store/question_answer.html')


@login_required(login_url='login')
def create_product(request):
    form = CreateProductForm()
    if request.method == "POST":
        form = CreateProductForm(request.POST, request.FILES)

        if form.is_valid():
            fm = form.save(commit=False)
            fm.user = request.user
            fm.save()
            return redirect('home')
        else:
            messages.error(request, "An error occurred")
    context = {
        'form': form
    }
    return render(request, 'store/new_product.html', context)


@login_required(login_url='login')
def delete_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        product.delete()
        return redirect(request.META.get("HTTP_REFERER"))

    return render(request, 'store/delete_product.html')


@login_required(login_url='login')
def product_update(request, product_id):
    product = Product.objects.get(id=product_id)
    form = CreateProductForm(instance=product)

    if request.user.id != product.user.id:
        return HttpResponse("You are not permitted to update this product")
    else:
        if request.method == "POST":
            form = CreateProductForm(request.POST, request.FILES, instance=product)

            if form.is_valid():
                form.save()
                return redirect('home')
        context = {
            "form": form
        }
        return render(request, 'store/product_update.html', context)


def admin(request):
    categories = Category.objects.all()
    num_category = Category.objects.all().count()
    products = Product.objects.all()
    context = {
        'category': categories,
        'num_category': num_category,
        'products': products
    }
    return render(request, 'store/admin/admin.html', context)


def remove_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    product.status = not product.status
    product.save()
    return redirect('admin')


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        customer = request.user
        user = User.objects.all()
        cart = Cart.objects.filter(user=customer)
        if not cart.exists():
            # create a new cart and add the selected item to cart
            cart = Cart.objects.create(user=customer, completed=False)
            CartItem.objects.create(cart=cart, quantity=1, product=product)
        else:
            # get cart item and increment quantity
            cart_item = CartItem.objects.filter(cart=cart, product=product)
            cart_item.quantity += 1
        messages.success(request, "Item added to cart")
        return redirect("view-cart")
    except CartItem.DoesNotExist:
        messages.error(request, "You must be logged in to add to cart")
        return redirect("login")

    return redirect(request.META.get('HTTP_REFERER'))


def view_cart(request):
    customer = request.user
    if customer.is_authenticated:
        cart = Cart.objects.filter(user=customer)[:1]
        cartitems = CartItem.objects.filter(cart=cart)
    else:
        cart = None
        cartitems = None
        cart = {'cartquantity': 0}
        messages.error(request, "You have to be logged in to view this page")
        return redirect("login")
    context = {
        'cart': cart,
        'cartitems': cartitems,
    }

    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        cart, created = Cart.objects.get_or_create(user=customer, completed=False)
        cartitems = cart.cartitem_set.all()
    else:
        cart = []
        cartitems = []
        cart = {'cartquantity': 0}
    context = {'cart': cart, 'cartitems': cartitems}
    return render(request, 'store/checkout.html', context)


def quantity_increment(request, product_id):
    cartitem = get_object_or_404(CartItem, id=product_id)
    cartitem.quantity += 1
    cartitem.save()
    return redirect(request.META.get('HTTP_REFERER'))


def quantity_decrement(request, pk):
    cartitem = get_object_or_404(CartItem, id=pk)
    if cartitem.quantity > 1:
        cartitem.quantity -= 1
        cartitem.save()
    else:
        messages.error(request, 'Quantity can not be zero')
    return redirect(request.META.get('HTTP_REFERER'))


def shopping_completed(request, pk):
    product_history = {}
    if request.user.is_authenticated:
        cartitem = get_object_or_404(CartItem, id=pk)
        code = request.POST.get('coupon')
        if code.lower() == 'go shopping':
            product_history[cartitem.product_id] = cartitem.product
        else:
            messages.error(request)
