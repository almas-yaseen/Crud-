from django.urls import path
from .import views



urlpatterns = [
    path('', views.home,name='home'),
    path('products/', views.products,name='products'),
    path('customer/<str:pk>/', views.customer,name='customer'),
    path('createOrder/<str:pk>/',views.createOrder,name='createOrder'),
    path('updateOrder/<str:pk>/',views.updateOrder,name='updateOrder'),
    path('delete/<str:pk>/',views.delete,name='delete'),
    path('login/',views.loginPage,name='login'),
    path('register/',views.register,name='register'),
    path('logout/',views.logoutUser,name='logout'),
    
]
