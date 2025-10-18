from django.shortcuts import render, redirect, get_object_or_404
from .models import MenuCategory, MenuItem, Restaurant
from customer.models import Order, OrderItem
from .forms import CategoryForm, MenuItemForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST

import qrcode
from io import BytesIO
import base64
from .models import Table

def is_owner_or_superuser(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)

owner_required = user_passes_test(is_owner_or_superuser)

def get_user_restaurant(user):
    return get_object_or_404(Restaurant, owner=user)

@owner_required
def dashboard_view(request):
    context = {
        "owner_name": request.user.full_name,
        "restaurant_name": None,
    }

    if not request.user.is_superuser:
        restaurant = get_user_restaurant(request.user)
        context["restaurant_name"] = restaurant.name

    return render(request, "restaurant/dashboard.html", context)

@owner_required
def menu_view(request):
    restaurant = get_object_or_404(Restaurant, owner=request.user)
    categories = MenuCategory.objects.filter(restaurant=restaurant).order_by('display_order')
    selected_category = request.GET.get("category")
    if selected_category and selected_category != "all":
        items = MenuItem.objects.filter(category__id=selected_category, category__restaurant=restaurant)
    else:
        items = MenuItem.objects.filter(category__restaurant=restaurant)

    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            new_category = form.save(commit=False)
            new_category.restaurant = restaurant
            new_category.display_order = MenuCategory.objects.filter(restaurant=restaurant).count() + 1
            new_category.save()
            return redirect("menu")
    else:
        form = CategoryForm()

    context = {
        "categories": categories,
        "items": items,
        "form": form,
        "selected_category": int(selected_category) if selected_category and selected_category.isdigit() else None
    }
    return render(request, "restaurant/menu.html", context)

@owner_required
def edit_category_view(request, category_id):
    category = get_object_or_404(MenuCategory, id=category_id, restaurant__owner=request.user)

    if request.method == "POST":
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            form.save()
            return redirect("menu")
    return redirect("menu")

@owner_required
def delete_category_view(request, category_id):
    category = get_object_or_404(MenuCategory, id=category_id, restaurant__owner=request.user)
    category.delete()
    return redirect("menu")

@owner_required
def add_item_view(request, item_id=None):
    restaurant = get_user_restaurant(request.user)

    if item_id:
        item = get_object_or_404(MenuItem, id=item_id, category__restaurant=restaurant)
        title = "Edit Menu Item"
    else:
        item = None
        title = "Add New Menu Item"

    if request.method == "POST":
        form = MenuItemForm(request.POST, instance=item, restaurant=restaurant)
        if form.is_valid():
            menu_item = form.save(commit=False)
            menu_item.save()
            return redirect("menu")
    else:
        form = MenuItemForm(instance=item, restaurant=restaurant)

    return render(request, "restaurant/additem.html", {"form": form, "title": title})

@owner_required
def delete_item_view(request, item_id):
    restaurant = get_user_restaurant(request.user)
    item = get_object_or_404(MenuItem, id=item_id, category__restaurant=restaurant)
    item.delete()
    return redirect("menu")

@owner_required
def orders_view(request):
    restaurant = get_user_restaurant(request.user)
    orders = Order.objects.filter(table__restaurant=restaurant).prefetch_related("order_items__menu_item", "table")

    return render(request, "restaurant/orders.html", {"orders": orders})

@owner_required
@require_POST
def update_order_status(request, order_id):
    restaurant = get_user_restaurant(request.user)
    order = get_object_or_404(Order, id=order_id, table__restaurant=restaurant)
    new_status = request.POST.get("status")

    if new_status in ["pending", "preparing", "completed"]:
        order.status = new_status
        order.save()

    return redirect("owner_orders")

@owner_required
def qr_generator_view(request):
    restaurant = get_user_restaurant(request.user)
    tables = restaurant.tables.all()

    qr_codes = []
    for table in tables:
        table_number = table.table_number
        url = f"https://infs3202-1e372ad6.uqcloud.net/tabletap/customer/table/{restaurant.id}/{table_number}"
        qr = qrcode.QRCode(version=1, box_size=10, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color="white")
        
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        img_base64 = base64.b64encode(buffer.getvalue()).decode()
        qr_codes.append({
            "table_number": table_number,
            "qr_code": f"data:image/png;base64,{img_base64}",
        })

    return render(request, "restaurant/qrcode.html", {
        "qr_codes": qr_codes,
        "restaurant_name": restaurant.name,
    })
