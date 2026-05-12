from django.shortcuts import render
from products.models import Product,Category
from vendors.models import Vendor
from orders.models import Order
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseForbidden
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your views here.
def home(request):
    latest_products=Product.objects.order_by('-id')[:8]
    return render(request,'core/home.html',{'latest_products':latest_products})

@staff_member_required
def admin_dashboard(request):
    if request.user.role != 'admin':
        return HttpResponseForbidden("Access denied")

    context = {
        # stats
        'total_users': User.objects.count(),
        'total_vendors': Vendor.objects.count(),
        'total_products': Product.objects.count(),
        'total_orders': Order.objects.count(),

        # lists (latest data)
        'users': User.objects.all().order_by('-id')[:5],
        'vendors': Vendor.objects.select_related('user').all().order_by('-id')[:5],
        'products': Product.objects.select_related('vendor').all().order_by('-id')[:5],
    }

    return render(request, 'admin/dashboard.html', context)

def product_list(request):
    category_id = request.GET.get('category')
    products = Product.objects.all()
    categories = Category.objects.all()
    print("CATEGORY PARAM:", category_id)
    if category_id and category_id.isdigit():
        products = products.filter(category_id=int(category_id))
    return render(request, 'core/products.html', {'products': products,'categories': categories})

def search_products(request):
    query=request.GET.get('q')
    if query:
        products=Product.objects.filter(name__icontains=query)
    else:
        products=Product.objects.none()
    return render(request,'core/search.html',{'products':products,'query':query})