from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from .forms import OrderForm,CreateUserForm
from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .decorators import  unauthenticated_user,allowed_users,admin_only

# Create your views here.


@login_required(login_url='login')
@admin_only
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
@login_required(login_url='login')
def products(request):
     products = Product.objects.all()
     return render(request,'product.html',{'products':products})


@login_required(login_url='login')
def customer(request,pk):
     customer = Customer.objects.get(id=pk)
     orders = customer.order_set.all()
     order_count = orders.count()
     myFilter = OrderFilter(request.GET,queryset=orders)
     orders = myFilter.qs
     context = {
          'customer':customer,
          'order_count':order_count,
          'orders':orders,
          'myFilter':myFilter,
     }
     return render(request,'customer.html',context)



@login_required(login_url='login')
def createOrder(request,pk):
     OrderFormSet = inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
     customer = Customer.objects.get(id=pk)
     formset = OrderFormSet(queryset =Order.objects.none(), instance=customer)
     # form = OrderForm(initial={'customer':customer})
     if request.method == 'POST':
          # form = OrderForm(request.POST)
          formset = OrderFormSet(request.POST,instance=customer)
          if formset.is_valid():
               formset.save()
               return redirect('/')
               
     context={
          'formset':formset,
      
          
          
     }
     return render(request,'order_form.html',context)



@login_required(login_url='login')
def updateOrder(request,pk):
     order = Order.objects.get(id=pk)
     form = OrderForm(instance=order)
     if request.method == 'POST':
          form = OrderForm(request.POST,instance=order)
          if form.is_valid():
               form.save()
               return redirect('/')
     
     
     
     context = {
          'form':form,
          'order':order,
     }
     return render(request,'order_form.html',context)


@login_required(login_url='login')
def delete(request,pk):
     order = Order.objects.get(id=pk)
     if request.method=="POST":
          order.delete()
          return redirect('/')
          
          
     
     context ={'item':order}
     return render(request,'delete.html',context)


def logoutUser(request):
     logout(request)
     return redirect('login')
     
     


   
@unauthenticated_user
def loginPage(request):
          if request.method=="POST":
               username=request.POST.get('username')
               password = request.POST.get('password')
               user = authenticate(request,username=username,password=password)
               if user is not None:
                    login(request,user)
                    return redirect('home')
               else:
                    messages.info(request,'Username or Password is incorrect')
                    
               
          
          
          return render(request,'login.html')

@unauthenticated_user
def register(request):
     if request.user.is_authenticated:
          return redirect('home')
     else:
          form = UserCreationForm()
          if request.method =="POST":
               form = CreateUserForm(request.POST)
               if form.is_valid():
                    form.save()
                    user = form.cleaned_data.get('username')
                    messages.success(request,'Account was created for ' + user)
                    return redirect('login')
               
          

     context = {
          'form':form
     }
     return render(request,'registration.html',context)