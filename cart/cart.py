from store.models import Product, Profile

class Cart():
    def __init__(self, request):
        self.session = request.session 
        self.request = request 
        #get curennt session key if exist
        cart = self.session.get('session_key')

        #if the user is new, assign a new session key
        if 'session_key' not in request.session:
            cart= self.session['session_key'] = {}

        #Make sure cart is availabke on every pages of site 
        self.cart=cart 


    def db_add(self,product,quantity):
        product_id = str(product)
        product_qty= str(quantity)

        #logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user= Profile.objects.filter(user__id=self.request.user.id)
            # convert dict to str 
            carty = str(self.cart)
            carty= carty.replace("\'","\"")
            #save cartty to profile
            current_user.update(old_cart=str(carty))


    def add(self,product,quantity):
        product_id = str(product.id)
        product_qty= str(quantity)

        #logic
        if product_id in self.cart:
            pass
        else:
            # self.cart[product_id] = {'price':str(product.price)}
            self.cart[product_id] = int(product_qty)

        self.session.modified = True

        # deal with logged in user
        if self.request.user.is_authenticated:
            #get the current user profile
            current_user= Profile.objects.filter(user__id=self.request.user.id)
            # convert dict to str 
            carty = str(self.cart)
            carty= carty.replace("\'","\"")
            #save cartty to profile
            current_user.update(old_cart=str(carty))

    def __len__(self):
        return len(self.cart)
    
    def get_prods(self):
        #Gets ids form cart
        product_ids = self.cart.keys()
        #Use ids to look products in db
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):
        quantities =self.cart
        return quantities
    
    def update(self,product,quantity):
        product_id = str(product)
        product_qty = int(quantity)

        #get cart
        ourcart = self.cart

        #update dicionary
        ourcart[product_id] = product_qty
        self.session.modified = True

        if self.request.user.is_authenticated:
            #get the current user profile
            current_user= Profile.objects.filter(user__id=self.request.user.id)
            # convert dict to str 
            carty = str(self.cart)
            carty= carty.replace("\'","\"")
            #save cartty to profile
            current_user.update(old_cart=str(carty))

        thing=self.cart
        return thing
    
    def delete(self,product):
        product_id = str(product)
        # delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified=True

        if self.request.user.is_authenticated:
            #get the current user profile
            current_user= Profile.objects.filter(user__id=self.request.user.id)
            # convert dict to str 
            carty = str(self.cart)
            carty= carty.replace("\'","\"")
            #save cartty to profile
            current_user.update(old_cart=str(carty))

    def cart_total(self):
        #get product ids
        product_ids=self.cart.keys()

        # look up those keys in db
        products=Product.objects.filter(id__in=product_ids)
        # get quantities 
        quantities= self.cart
        total = 0
        for key,value in quantities.items():
            key=int(key)
            for product in products:
                if product.id == key:
                    if product.is_sale:
                        total += product.sale_price * value
                    else:
                        total += product.price * value
        return total    