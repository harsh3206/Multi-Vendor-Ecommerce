from django.urls import path
from accounts import views
urlpatterns = [
    path('signup/',views.signup,name='signup'),
    path('login/',views.uv_login,name='login'),
    path('logout/', views.uv_logout, name='logout'),
]
