from django.shortcuts import render,redirect, get_object_or_404
from .cart import Cart
from store. models import Product
from django.http import JsonResponse
from django.contrib import messages


# Create your views here.

def cart_summary(request):
    cart = Cart(request)
    cart_products=cart.get_prods
    quantities=cart.get_quants
    totals=cart.cart_total()
    return render(request, 'cart_summary.html',{"cart_products":cart_products,"quantities":quantities,'total':totals})

def cart_add(request):
    #Get cart
    cart=Cart(request)
    #test for post
    if request.POST.get('action')=='post':
        #Get stuff
        product_id= int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        # look product in database
        product = get_object_or_404(Product,id=product_id)
        # Save to session
        cart.add(product=product,quantity=product_qty)

        # Get Cart Quantity
        cart_quantity = cart.__len__()


        # return responce
        # response =JsonResponse({'Product Name ': product.name})
        response =JsonResponse({'qty': cart_quantity})
        messages.success(request,("Product Added to Cart"))
        return response

def cart_update(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        

        cart.update(product=product_id,quantity=product_qty)
        response=JsonResponse({'qty':product_qty})
        messages.success(request,("Your Cart has been updated"))
        return response

def cart_delete(request):
    cart=Cart(request)
    if request.POST.get('action')=='post':
        print(request)
        product_id = int(request.POST.get('product_id'))
        # call delete product 
        cart.delete(product_id)

        response= JsonResponse({'product':product_id})
        messages.success(request,("Item has been removed"))
        return response
    