from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Category, Product
from vendors.models import Vendor

def add_products(request):
    if request.user.role != 'vendor':
        return HttpResponse("Access denied")

    subcategories = Category.objects.filter(parent__isnull=False)

    vendor = get_object_or_404(Vendor, user=request.user)

    if request.method == "POST":
        name = request.POST['name']
        price = request.POST['price']
        description = request.POST['description']
        stock = request.POST['stock']
        image = request.FILES.get('image')

        subcategory = get_object_or_404(Category, id=request.POST['subcategory'])

        Product.objects.create(
            vendor=vendor,
            name=name,
            price=price,
            description=description,
            stock=stock,
            image=image,
            category=subcategory
        )

        return redirect('vendor_products')

    return render(request, 'products/add_products.html', {
        'subcategories': subcategories
    })

def product_list(request):
    products = Product.objects.filter(vendor__user=request.user)
    return render(request, 'products/product_list.html', {
        'products': products
    })

def edit_product(request, id):
    product = get_object_or_404(Product, id=id, vendor__user=request.user)

    subcategories = Category.objects.filter(parent__isnull=False)

    if request.method == "POST":
        product.name = request.POST.get('name')
        product.price = request.POST.get('price')
        product.stock = request.POST.get('stock')
        product.description = request.POST.get('description')

        subcategory_id = request.POST.get('subcategory')
        if subcategory_id:
            product.category = get_object_or_404(Category, id=subcategory_id)

        image = request.FILES.get('image')
        if image:
            product.image = image

        product.save()
        return redirect('product_list')

    return render(request, 'products/edit_products.html', {
        'product': product,
        'subcategories': subcategories
    })

def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_details.html', {
        'product': product
    })

def delete_product(request,id): 
    product=Product.objects.get(id=id,vendor__user=request.user)
    if request.method=="POST":
        product.delete()
        return redirect('product_list')
    return render(request,'products/delete_products.html',{'product':product})