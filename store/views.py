# admin
# username=Aman
# password=Aman@123

# user1
# username=Ammar
# password=Amaan@1234

#8.07





from django.shortcuts import render,redirect
from .models import Product , Category , Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm,UpdateUserForm,ChangePasswordForm,UserInfoForm


from payment.forms import ShippingForm
from payment.models import ShippingAddress


from django import forms 
from django.contrib import messages
from django.db.models import Q
import json  
from cart.cart import Cart

# Create your views here.



def search(request):
    # determine if they filled the form 
    if request.method == "POST":
        searched = request.POST["searched"]
        # query the database for the searched item
        searched = Product.objects.filter(Q(name__icontains=searched) | Q(description__icontains=searched))

        if not searched:
            messages.success(request,"Product not found ")
            return render(request, 'search.html',{})
        else:
             return render(request, 'search.html', {'searched': searched})
    else:
        return render(request, 'search.html',{})

    return render(request,'search.html',{})



def update_info(request):
    if request.user.is_authenticated:
        current_user=Profile.objects.get(user__id=request.user.id)
        #Get curent Users Shipping info 
        shipping_user=ShippingAddress.objects.get(user__id=request.user.id)
        # Get original user form
        form= UserInfoForm(request.POST or None,instance=current_user)

        #get users shipping form
        shipping_form=ShippingForm(request.POST or None, instance=shipping_user)


        if form.is_valid() or shipping_form.is_valid():
            #save originl form 
            form.save()
            #save shipping form 
            shipping_form.save()
            messages.success(request,"Your Info has been updated")
            return redirect('home')
        return render(request,'update_info.html',{'form':form,'shipping_form':shipping_form})
    else:
        messages.success(request,"You have to be logged in to update your profile")
        return redirect('home') 



def update_password(request):
        if request.user.is_authenticated:
            current_user=request.user
            if request.method == 'POST':
                form = ChangePasswordForm(current_user,request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Password changed successfully')
                    login(request,current_user)
                    return redirect('update_user')
                else:
                    for error in list(form.errors.values()):
                        messages.error(request, error)
                        return redirect('update_password')
            else:
                form= ChangePasswordForm(current_user)
                return render(request,'update_password.html',{'form':form})
        else:
            messages.success(request,'You must be logged in to change your password')
            return redirect('login')


def update_user(request):
    if request.user.is_authenticated:
        current_user=User.objects.get(id=request.user.id)
        user_form= UpdateUserForm(request.POST or None,instance=current_user)

        if user_form.is_valid():
            user_form.save()
            login(request,current_user)
            messages.success(request,"Your profile has been updated")
            return redirect('home')
        return render(request,'update_user.html',{'user_form':user_form})
    else:
        messages.success(request,"You have to be logged in to update your profile")
        return redirect('home') 


def category_summary(request):
    categories= Category.objects.all()
    return render(request,'category_summary.html',{'categories':categories})




def category(request,foo):
    # replace - to " "
    foo = foo.replace('-'," ")
    # Grab the category from url
    

    try:
        # Look up the category
        category = Category.objects.get(name=foo)
        products = Product.objects.filter(category=category)
        return render(request, 'category.html', {'products': products, 'category': category})
    except Exception as e:
        messages.success(request, f"Category does not exist. Error: {e}")
        return redirect('home')

    

def product(request,pk):
    product= Product.objects.get(id=pk)
    return render(request, 'product.html',{"product":product})


def home(request):
    products =Product.objects.all()
    return render(request,'home.html',{'products':products})


def about(request):
    return render(request,'about.html',{})


def login_user(request):
    if request.method == "POST":
        username =request.POST["username"]
        password =request.POST["password"]
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)

            # do some shopping cart stuff
            current_user = Profile.objects.get(user__id=request.user.id)
            # get their saved cart from the database
            saved_cart = current_user.old_cart

            #convert db string to dict
            if saved_cart:
                # convert to dict using json
                converted_cart=json.loads(saved_cart)

                #add the loaded dict to our session
                #get the cart
                cart=Cart(request)
                #loop thru the cart and add items from the db
                for key,value in converted_cart.items():
                    cart.db_add(product=key,quantity=value) 



            messages.success(request,("You Have been Logged IN"))
            return redirect('home')
        else:
            messages.success(request,("There is an error , Please try again "))
            return redirect('login')

    return render(request,'login.html',{})


def logout_user(request):
    logout(request)
    messages.success(request,("You have Been Successfully logged out"))
    return redirect('home')


def register_user(request):
    form= SignUpForm()
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username= form.cleaned_data['username']
            password= form.cleaned_data['password1']
            #log in user
            user = authenticate(username=username,password=password)
            login(request,user)
            messages.success(request,("You have Been Successfully Registered - Please fill Your info"))
            return redirect('update_info')
        else:
            messages.success(request,("Whoops there is a problem while registering"))
            return redirect('register')
    else:
        return render(request,'register.html',{'form':form})

            


