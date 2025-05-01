from django.shortcuts import render , redirect ,get_object_or_404
from .models import Category,Products,AddCart,Profile,I,Payment,Buynow,Banner
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate , login ,logout
from django.http import HttpResponse
from datetime import  timedelta
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.
def home(request):
    context={
        'cat':Category.objects.all(),
        'image':I.objects.all(),
        'product':Products.objects.all(),
        'ibanners':Banner.objects.all()
    }
    return render(request,'home.html',context)
def display_cat(request,ids):
    cat=Category.objects.get(id=ids)
    products=Products.objects.filter(category=cat)
    context={
        'products':products
    }
    return render(request,'products.html',context)
def search(request):
    product=None
    if request.method=="POST":
        q=request.POST.get('q')
        if q:
            product=Products.objects.filter(title__contains=q )
    context={
        'pro':product,
        'msg':'product not fond'
    }
    return render(request,'search.html',context)
def display_products(request,ids):
    products=Products.objects.get(id=ids)
    context={
        'pro':products
    }
    return render(request,'dproducts.html',context)
def signup_views(request):
    if request.user.is_authenticated:
        return redirect('login')
    if request.method=="POST":
        un=request.POST.get('un')
        e=request.POST.get('e')
        p1=request.POST.get('p1')
        p2=request.POST.get('p2')
        if p1==p2:
            if not User.objects.filter(username=un).exists():
                User.objects.create_user(username=un,email=e,password=p1)
                return redirect('login')
            else:
                return render(request,'signup.html',{'msg':'Username is alreday present '})
        else:
             return render(request,'signup.html',{'msg':'password is invalid '})
    return render(request,'signup.html')
def login_views(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method=="POST":
        un=request.POST.get('un')
        p1=request.POST.get('p1')
        user=authenticate(request,username=un,password=p1)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            return render(request,'login.html',{'msg':'invalid credientals'})
    return render(request,'login.html')     
def logout_views(request):
    user=logout(request)
    return redirect('login')
def add_cart(request,ids):
    if not request.user.is_authenticated:
        return redirect('login')
    product=Products.objects.get(id=ids)
    addcarts= AddCart.objects.filter(products=product ,user=request.user).first()
    if addcarts :
        if addcarts.quantity >=1:
            addcarts.quantity +=1
            addcarts.save()
    else:
        AddCart.objects.create(products=product,user=request.user)
    a_cart=AddCart.objects.filter(user=request.user)
    context={
        'cart':a_cart
    }
    return render(request,'addcart.html',context)
def remove_cart(request,ids):
    addcart=AddCart.objects.get(id=ids)
    if addcart.quantity >1:
        addcart.quantity -=1
        addcart.save()
    else:
        addcart.delete()
        return  redirect('display')
    return redirect('display')
    
def display_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    context={
        'cart':AddCart.objects.filter(user=request.user)
    }
    return render(request,'dispaly_cart.html',context)



def buynow(request, ids):
    if not request.user.is_authenticated:
        return redirect('login')
    pro = get_object_or_404(Products, id=ids)
    buy = Buynow.objects.filter(products=pro, user=request.user).first() or None  

    if request.method == "POST":
        pay_method = request.POST.get("pay")

        # Validate payment method
        payment_instance = Payment.objects.filter(payment_method=pay_method).first()
        if not payment_instance:
            messages.error(request, "Invalid payment method.")
            return redirect('buynow', ids=ids)

        # Create order
        delivery_date = timezone.now().date() + timedelta(days=5)
        new_buy = Buynow.objects.create(
            products=pro, 
            user=request.user, 
            total=1, 
            payment=payment_instance,
            delivary_date=delivery_date
        )

        messages.success(request, "Order placed successfully!")
        return redirect('orders')  # Redirect after success

    context = {
        "pro": pro, 
        "payment": Payment.objects.all(),
        "buy": buy,  # Ensure buy is either an object or None
        "ibanners": Banner.objects.all()
    }
    return render(request, "buynow.html", context)


def display_order(request):
    if not request.user.is_authenticated:
        return redirect('login')
    buy = Buynow.objects.filter(user=request.user)
    context = {'buy': buy}
    return render(request, 'orders.html', context)
def delete_order(request,ids):
    buys=Buynow.objects.get(id=ids)
    buys.delete()
    return redirect('orders')
from django.core.mail import EmailMessage

def order_success(request , ids):
    user_email = request.user.email  # Get the logged-in user's email
    pro = Products.objects.get(id=ids)  # Replace with actual order ID

    if user_email:  # Ensure email is not empty
        email = EmailMessage(
            "Order Placed Successfully",
            f"Dear Customer,\n\nYour order with ID {pro.title} has been placed successfully!\n\n"
            "Please find the product image attached.\n\n"
            "Thank you for shopping with us.",
            settings.EMAIL_HOST_USER,
            [user_email],
        )

        # Attach the product image
        if pro.image:
            with open(pro.image.path, "rb") as img:
                email.attach(pro.image.name, img.read(), "image/jpeg")  # Change MIME type if needed

        email.send()
        return HttpResponse("Order placed successfully. Confirmation email sent.")  
    
    return HttpResponse("Error: No email found for the user.", status=400)

