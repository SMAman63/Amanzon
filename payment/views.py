from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm,PaymentForm
from payment.models import ShippingAddress,Order,OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product,Profile
import datetime


# Create your views here.

def orders(request,pk):
    if request.user.is_authenticated and request.user.is_superuser:
        order= Order.objects.get(id=pk)
        # get order item
        items = OrderItem.objects.filter(order=pk)

        if request.POST:
            status = request.POST['shipping_status']
            #check if true or f
            if status == 'true':
                # get the order 
                order=Order.objects.filter(id=pk)
                #update the status
                now=datetime.datetime.now()
                order.update(shipped=True,date_shipped=now )
            else:
                order=Order.objects.filter(id=pk)
                #update the status
                order.update(shipped=False)
            messages.success(request,"shipping order updated")
            return redirect('home')


        return render(request,'orders.html',{"order":order,"items":items})
    
    else:
        messages.success(request,'Access Denied')
        return redirect('home')


def not_shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders=Order.objects.filter(shipped=False)
        if request.POST:
            status = request.POST['shipping_status']
            num=request.POST['num']
            #check if true or f
            order = Order.objects.filter(id=num)

            now=datetime.datetime.now()
            order.update(shipped=True,date_shipped=now )
            
            messages.success(request,"shipping order updated")
            return redirect('home')
        return render(request, 'not_shipped_dash.html',{"orders":orders})
    else:
        messages.success(request,'Access Denied')
        return redirect('home')



def shipped_dash(request):
    if request.user.is_authenticated and request.user.is_superuser:
        orders=Order.objects.filter(shipped=True)
        if request.POST:
            status = request.POST['shipping_status']
            num=request.POST['num']
            #check if true or f
            order = Order.objects.filter(id=num)
            now=datetime.datetime.now()
            order.update(shipped=False )
            
            messages.success(request,"shipping order updated")
            return redirect('home')
        return render(request, 'shipped_dash.html',{"orders":orders})
    else:
        messages.success(request,'Access Denied')
        return redirect('home')





def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products=cart.get_prods
        quantities=cart.get_quants
        totals=cart.cart_total()


        #get billing info from  the last page
        payment_form=PaymentForm(request.POST or None)
        # get shipping session date
        my_shipping = request.session.get('my_shipping')

        # Gather user info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']
         # lets create shipping addr from session info
        shipping_address=f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_zipcode']}\n"
        amount_paid = totals

        if request.user.is_authenticated:
            user = request.user
            #create order
            create_order = Order(user=user, full_name=full_name , email=email,shipping_address=shipping_address,amount_paid=amount_paid )
            create_order.save()  

            #add order items
            #get product info
            order_id = create_order.pk

            #get product info
            for product in cart_products():
                #get product id
                product_id = product.id
                #get product price
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price

                for key,value in quantities().items():
                    if int(key)==product.id:
                        #create order item
                        create_order_item=OrderItem( order_id=order_id,product_id=product_id,user=user,quantity=value,price=price )
                        create_order_item.save() 

            #delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete the key
                    del request.session[key]

            #delete Cart from database(old_cart field)
            current_user = Profile.objects.filter(user__id=request.user.id)
            #delete shopping cart in db 
            current_user.update(old_cart="")


            messages.success(request,'Order Placed!')
            return redirect('home')
        

        else:
            create_order = Order(full_name=full_name , email=email,shipping_address=shipping_address,amount_paid=amount_paid )
            create_order.save()

            #add order items
            #get product info
            order_id = create_order.pk

            #get product info
            for product in cart_products():
                #get product id
                product_id = product.id
                #get product price
                if product.is_sale:
                    price=product.sale_price
                else:
                    price=product.price

                for key,value in quantities().items():
                    if int(key)==product.id:
                        #create order item
                        create_order_item=OrderItem( order_id=order_id,product_id=product_id,quantity=value,price=price )
                        create_order_item.save()   

            #delete our cart
            for key in list(request.session.keys()):
                if key == "session_key":
                    #delete the key
                    del request.session[key]


            messages.success(request,'Order Placed!')
            return redirect('home')

       
     
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products=cart.get_prods
        quantities=cart.get_quants
        totals=cart.cart_total()

        #create a session with shipping info
        my_shipping=request.POST
        request.session['my_shipping']=my_shipping 

        #Check to see if user is logged in
        if request.user.is_authenticated:
            # Get The Billing Form 
            billing_form= PaymentForm()
            return render(request, 'billing_info.html',{"cart_products":cart_products,"quantities":quantities,'total':totals,'shipping_info':request.POST,'billing_form':billing_form})
        else:
            billing_form= PaymentForm()
            return render(request, 'billing_info.html',{"cart_products":cart_products,"quantities":quantities,'total':totals,'shipping_info':request.POST,'billing_form':billing_form})
            




        shipping_form=request.POST
        return render(request, 'billing_info.html',{"cart_products":cart_products,"quantities":quantities,'total':totals,'shipping_form':shipping_form})
    else:
        messages.success(request,"Access Denied")
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    cart_products=cart.get_prods
    quantities=cart.get_quants
    totals=cart.cart_total()

    if request.user.is_authenticated:
        # Checkout as logged in user
        #Shipping User
        shipping_user=ShippingAddress.objects.get(user__id=request.user.id)
        #Shipping Form   
        shipping_form=ShippingForm(request.POST or None, instance=shipping_user)
        return render(request, 'checkout.html',{"cart_products":cart_products,"quantities":quantities,'total':totals,'shipping_form':shipping_form})
    else:
        # Checkout as guest
        shipping_form=ShippingForm(request.POST or None)
        return render(request, 'checkout.html',{"cart_products":cart_products,"quantities":quantities,'total':totals,'shipping_form':shipping_form})






def payment_success(request):
    return render(request,"payment_success.html",{})
    
