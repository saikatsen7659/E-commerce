from django.shortcuts import render , redirect
from django.views import View
from .models import Product , Customer, Cart, OrderPlaced , Payment , Wishlist
from django.db.models import Count
from .forms import RegistationForm , ProfileForm
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Q
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


# Create your views here.
@login_required
def home(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))
    return render(request,"pages/home.html",locals())

@login_required
def about(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishlist = len(Cart.objects.filter(user=request.user))
    return render(request,"pages/about.html",locals())

@login_required
def contact(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))
    return render(request,"pages/contact.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryView(View):
    def get(self, request, val):
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))   
        product = Product.objects.filter(category = val)
        title = Product.objects.filter(category = val).values('title')
        return render(request, "pages/category.html",locals())

@method_decorator(login_required,name='dispatch')
class CategoryTitle(View):
    def get(self, request, val):
        product = Product.objects.filter(title=val)
        title = Product.objects.filter(category=product[0].category).values('title')
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))
        return render(request, "pages/category.html",locals())
    
@method_decorator(login_required,name='dispatch')
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk = pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user)) 
        return render(request,"pages/productdetail.html",locals())
    
@method_decorator(login_required,name='dispatch')
class RegistationView(View):
    def get(self, request):
        form = RegistationForm()
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))
        return render(request, 'pages/registation.html',locals())
    
    def post(self,request):
        form = RegistationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request, 'pages/registation.html',locals())
  
@method_decorator(login_required,name='dispatch')     
class ProfileView(View):
    def get(self, request):
        form = ProfileForm()
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))  
        return render(request, 'pages/profile.html',locals())

    def post(self,request):
        form = ProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user,name=name,locality=locality,city=city,mobile=mobile,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations")
            return redirect("address")
        else:
            messages.warning(request,"Invalid data")
        return render(request, 'pages/profile.html',locals())

@login_required 
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))  
    return render(request, 'pages/address.html',locals())

@login_required
def deleteaddress(request,pk):
    add = Customer.objects.get(pk=pk)
    add.delete()
    return redirect("profile")

@method_decorator(login_required,name='dispatch')
class updateAddress(View):
    def get(self,request,pk):
        add = Customer.objects.get(pk=pk)
        form = ProfileForm(instance=add)
        totalitem = 0
        wishlist = 0     
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user)) 
        return render(request, 'pages/updateAddress.html',locals())
        
    def post(self,request,pk):
        form = ProfileForm(request.POST)
        if form.is_valid():
            add = Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']            
            add.save()
            messages.success(request,"Congratulations")
        else:
            messages.warning(request,"Invalid data")
        return redirect("address")
  
  
@login_required  
def add_to_cart(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/cart")

@login_required
def show_cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = round((amount + value),2) 
        amount = round(amount,2)
    totalamount = amount + 50
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))  
    return render(request, 'pages/addcart.html',locals())


@method_decorator(login_required,name='dispatch')
class checkout(View):
    def get(self,request):
        totalitem = 0
        wishlist = 0
        if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))   
        user = request.user
        add = Customer.objects.filter(user=user)
        cart_items = Cart.objects.filter(user=user)
        amount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            amount = round((amount + value),2)
            amount = round(amount,2)
        totalamount = amount + 50
        razoramount = int(totalamount * 100)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        data = {"amount":razoramount,"currency": "INR", "receipt":"order_rcptid_11"}
        payment_response = client.order.create(data=data)
        
        order_id = payment_response['id']
        order_status = payment_response['status']
        if order_status == 'created':
            payment = Payment(
                user=user,
                amount=totalamount,
                razorpay_order_id=order_id,
                razorpay_payment_status=order_status
            )
            payment.save()
        return render(request, 'pages/checkout.html',locals())


@login_required  
def payment_done(request):
    order_id=request.GET.get('order_id')
    payment_id=request.GET.get('payment_id')  
    cust_id = request.GET.get('cust_id')
    user = request.user
    customer=Customer.objects.get(id=cust_id)
    payment=Payment.objects.get(razorpay_order_id=order_id)
    payment.paid = True 
    payment.razorpay_payment_id = payment_id
    payment.save()
    
    cart=Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
        c.delete()  
    return redirect("orders") 

@login_required
def orders(request):
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))  
    order_placed=OrderPlaced.objects.filter(user=request.user)
    return render (request, 'pages/orders.html',locals())   

@login_required  
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) 
        c.quantity = c.quantity + 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        amount_value = 0
        
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            amount_value = round(amount,2)
        totalamount = amount_value + 50
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        } 
        return JsonResponse(data)  

@login_required    
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) 
        c.quantity-=1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        amount_value = 0
        
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            amount_value = round(amount,2)
        totalamount = amount_value + 50
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        } 
        return JsonResponse(data) 
 
@login_required   
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user)) 
        c.delete()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount = 0
        amount_value = 0
        
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
            amount_value = round(amount,2)
        totalamount = amount_value + 50
        data={
            'amount':amount,
            'totalamount':totalamount
        } 
        return JsonResponse(data) 
    
    
@login_required  
def add_to_wishlist(request):
    user=request.user
    product_id = request.GET.get('prod_id')
    product = Product.objects.get(id=product_id)
    Cart(user=user,product=product).save()
    return redirect("/wishlist")

@login_required
def show_wishlist(request):
    user = request.user
    cart = Cart.objects.filter(user=user)
    amount = 0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = round((amount + value),2) 
        amount = round(amount,2)
    totalamount = amount + 50
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))  
    return render(request, 'pages/wishlist.html',locals())
 
@login_required 
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).save()
        data={
            'message':"Wishlist Added"
        }
        return JsonResponse(data)
 
@login_required   
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user,product=product).delete()
        data={
            'message':"Wishlist Removed"
        }
        return JsonResponse(data)
 
@login_required     
def search(request):
    query = request.GET["search"]
    totalitem = 0
    wishlist = 0
    if request.user.is_authenticated:
         totalitem = len(Cart.objects.filter(user=request.user))
         wishlist = len(Cart.objects.filter(user=request.user))
    product = Product.objects.filter(Q(title__icontains=query))
    return render (request,"pages/search.html",locals())
        
