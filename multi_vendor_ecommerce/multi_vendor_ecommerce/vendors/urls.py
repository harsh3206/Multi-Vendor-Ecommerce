from django.urls import path
from vendors import views
urlpatterns = [
    path('vendor/dashboard/',views.vendor_dashboard,name='vendor_dashboard'),
    path('vendor/profile/',views.vendor_profile,name='vendor_profile'),
    path('vendors/vendor/products/', views.vendor_products, name='vendor_products'),
    path('vendor/orders/', views.vendor_orders, name='vendor_orders'),
]
