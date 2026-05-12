from django.urls import path,include
from core import views
app_name='core'
urlpatterns = [
 path('',views.home,name="home"),
 path('dashboard/', views.admin_dashboard, name='admin_dashboard'),
 path('products/',views.product_list,name='product_list'),
 path('search/',views.search_products,name='search_products'),
]