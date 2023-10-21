from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm 

# Create your views here.



def home(request):
     orders = Order.objects.all()
     customers = Customer.objects.all()
     total_customers = customers.count()
     total_orders = orders.count()
     orders_delivered = orders.filter(status='DELIVERED').count()
     pending = orders.filter(status='PENDING').count()
     context = {
          'orders':orders,
          'customers':customers,
          'total_customers':total_customers,
          'total_orders':total_orders,
          'orders_delivered':orders_delivered,
          'pending':pending,
     }
     return render(request,'dashboard.html',context)

def products(request):
     products = Product.objects.all()
     return render(request,'product.html',{'products':products})

def customer(request,id):
     customer = Customer.objects.get(id=id)
     orders = customer.order_set.all()
     order_count = orders.count()
     context = {
          'customer':customer,
          'order_count':order_count,
     }
     return render(request,'customer.html',context)




def createOrder(request):
     form = OrderForm()
     if request.method == 'POST':
          form = OrderForm(request.POST)
          if form.is_valid():
               form.save()
               return redirect('/')
               
     context={
          'form':form
     }
     return render(request,'order_form.html',context)