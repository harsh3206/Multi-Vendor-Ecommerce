from django.shortcuts import render, redirect, get_object_or_404
from cart.models import Cart, CartItem
from orders.models import Order,VendorOrder,OrderItem
from django.db import transaction
from django.contrib.auth.decorators import login_required
import uuid


def generate_order_id():
    return str(uuid.uuid4()).replace('-', '')[:12].upper()


@login_required
def place_order(request):
    cart = get_object_or_404(Cart, user=request.user)
    items = cart.items.all()

    if not items.exists():
        return redirect('view_cart')

    with transaction.atomic():

        # ✅ Create Order
        order = Order.objects.create(
            user=request.user,
            order_id=generate_order_id(),
            total_amount=0
        )

        total = 0
        vendor_map = {}

        # ✅ Group items by vendor
        for item in items:
            vendor = item.product.vendor

            if vendor not in vendor_map:
                vendor_map[vendor] = []

            vendor_map[vendor].append(item)

        # ✅ Create VendorOrders + OrderItems
        from .models import VendorOrder  # import here if needed

        for vendor, vendor_items in vendor_map.items():
            vendor_total = 0

            vendor_order = VendorOrder.objects.create(
                order=order,
                vendor=vendor,
                total_amount=0
            )

            for item in vendor_items:
                item_total = item.quantity * item.product.price

                OrderItem.objects.create(
                    order=order,
                    vendor_order=vendor_order,
                    product=item.product,
                    vendor=vendor,
                    quantity=item.quantity,
                    price=item.product.price
                )

                vendor_total += item_total
                total += item_total

            vendor_order.total_amount = vendor_total
            vendor_order.save()

        # ✅ Update total
        order.total_amount = total
        order.save()

        # ✅ Clear cart
        items.delete()

    return redirect('order_success', order_id=order.id)

@login_required
def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_success.html', {'order': order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'orders/order_list.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    items = order.items.all()
    return render(request, 'orders/order_detail.html', {
        'order': order,
        'items': items
    })