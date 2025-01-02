from .cart import Cart

# crete contexxt prossesor so our cart can work on all page
def cart(request):
    # Return default data from our cart 
    return {'cart' : Cart(request)}