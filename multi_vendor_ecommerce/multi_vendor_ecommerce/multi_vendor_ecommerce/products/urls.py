from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static  
from products import views
urlpatterns = [
    path('products/add_products/',views.add_products,name="add_products"),
    path('products/product_list/',views.product_list,name="product_list"),
    path('products/delete/<int:id>/',views.delete_product,name="delete_product"),
    path('edit/<int:id>/', views.edit_product, name='edit_product'),
    path('product/<int:id>/',views.product_detail,name="product_detail")

]