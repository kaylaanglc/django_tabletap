from django.shortcuts import render, get_object_or_404, redirect
from restaurant.models import Table, Restaurant, MenuCategory, MenuItem
from .models import Order, OrderItem

def table_order_view(request, restaurant_id, table_number):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    table = get_object_or_404(Table, restaurant=restaurant, table_number=table_number)
    categories = MenuCategory.objects.filter(restaurant=restaurant).order_by('display_order')
    items = MenuItem.objects.filter(category__in=categories)

    categorized_items = {category: items.filter(category=category) for category in categories}
    error_message = None

    if request.method == "POST":
        valid_items = []
        for item in items:
            qty_str = request.POST.get(f"item_{item.id}", "")
            try:
                qty = int(qty_str)
                if qty > 0:
                    valid_items.append((item, qty))
            except (ValueError, TypeError):
                continue

        if not valid_items:
            error_message = "Please select at least one item to submit an order."
        else:
            order = Order.objects.create(table=table, status="pending")
            for item, qty in valid_items:
                OrderItem.objects.create(order=order, menu_item=item, quantity=qty)
            return redirect("confirmation", restaurant_id=restaurant_id, table_number=table_number)

    return render(request, "customer/table_order.html", {
        "restaurant": restaurant,
        "table": table,
        "categorized_items": categorized_items,
        "error_message": error_message
    })

def order_confirmation_view(request, restaurant_id, table_number):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)
    table = get_object_or_404(Table, restaurant=restaurant, table_number=table_number)

    latest_order = Order.objects.filter(table=table).order_by('-created_at').first()

    order_items = latest_order.order_items.select_related('menu_item') if latest_order else []
    total = sum(item.menu_item.price * item.quantity for item in order_items)

    return render(request, "customer/confirmation.html", {
        "restaurant": restaurant,
        "table": table,
        "order_items": order_items,
        "total": total,
    })
