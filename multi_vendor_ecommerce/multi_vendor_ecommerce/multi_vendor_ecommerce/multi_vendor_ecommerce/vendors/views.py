from django.shortcuts import render,redirect
from products.models import Product
from orders.models import OrderItem
# Create your views here.
def vendor_dashboard(request):
    if request.user.role != 'vendor':
        return redirect('/')
    return render(request,'vendors/vendor_dashboard.html')

from vendors.models import Vendor

def vendor_register(request):
    if request.method == "POST":
        shopname = request.POST['shopname']

        Vendor.objects.create(
            user=request.user,
            shopname=shopname
        )

        return redirect('vendor_dashboard')

    return render(request, 'vendors/vendor_registration.html')

def vendor_profile(request):
    if request.user.role!='vendor':
        return redirect('/')
    return render(request,'vendors/vendor_profile.html')

def vendor_products(request):
    vendor=Vendor.objects.get(user=request.user)
    products=Product.objects.filter(vendor=vendor)
    return render(request,'vendors/vendor_products.html',{'products':products})

def vendor_orders(request):
    vendor = request.user.vendor

    orders = OrderItem.objects.filter(
        product__vendor=vendor
    ).select_related('order', 'product').order_by('-order__created_at')

    return render(request, 'vendors/vendor_orders.html', {
        'orders': orders
    })