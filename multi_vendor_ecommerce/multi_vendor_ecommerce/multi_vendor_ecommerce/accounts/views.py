from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout,get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from vendors.models import Vendor
# Create your views here.
User = get_user_model()
def signup(request):
    if request.method=="POST":
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        confirmpassword=request.POST['password2']
        role=request.POST['role']
        if password!=confirmpassword:
            return render(request,'accounts/signup.html',{'error':'Passwords do not match'})
        user=User.objects.create_user(username=username,email=email,password=password,role=role)
        if role=='vendor':
            shop_name=request.POST.get('shop_name')
            Vendor.objects.create(user=user,shop_name=shop_name)
            return redirect('login')
        if role == 'vendor' and not shopname:
            return render(request, 'accounts/signup.html', {'error': 'Shop name is required'})
    return render(request,'accounts/signup.html')

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

def uv_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            if user.role == 'vendor':
                return redirect('vendor_dashboard')

            elif user.role == 'customer':
                return redirect('core:home')   

            else:
                return redirect('/admin/')

        else:
            return render(request, 'accounts/login.html', {
                'error': 'Invalid Username or Password'
            })
    return render(request, 'accounts/login.html')

@login_required
def uv_logout(request):
    logout(request)
    return redirect('login')