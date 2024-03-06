import json
import time
import os
from abc import abstractmethod




def checkAuthonication(username,password):
    with open("data.json","r") as f:
        response = json.load(f)
        users = response["users"]
        for user in users:
            if user["username"] == username and user["password"] == password:
                return True
        return False


def processJsonFileDecorator(func=None,shouldFileUpdate=True):
    def decorator(func):
        def wrapper(self,*args ,**kwargs):
            try:
                with open('data.json','r+') as f:
                    response = json.load(f)
                    result = func(self,response, *args, **kwargs)
                    if shouldFileUpdate:
                        f.seek(0)
                        json.dump(response,f,indent=2)
                        f.truncate()
                    return result
            except Exception as e:
                print(f"Something went wrong {e}")
                return None
        return wrapper
    if func is None:
        return decorator
    else: return decorator(func)


def checkFileExist():
    status = os.path.exists('data.json')
    if not status:
        with open("data.json","w+") as f:
            context = {
               "products":[
                       {
      "id": 1,
      "p_name": "Mango",
      "price": 30
    },
    
    {
      "id": 2,
      "p_name": "Apple",
      "price": 30
    },

    {
      "id": 4,
      "p_name": "Biscut",
      "price": 2
    }
               ],
               "users":[],
               "carts":[]
            }
            f.seek(0)
            json.dump(context,f,indent=2)
            f.truncate()
    return status



        
def discount_10_percent(func):
    def wrapper(self,response='',*args,**kwargs):
        user = next((user for user in response['users'] if user['username']==self.username),None)
        total_cost = func(self,response,*args,**kwargs)
        discount_Price = 0
        if user and user['isPremium']:
            discount_Price = total_cost*0.1
            total_cost = total_cost - discount_Price
        context = {
            'username':self.username,
            'userType':user['isPremium'],
            'discount_Price':float(discount_Price),
            'total_cost':float(total_cost)
        }
        return context
    
    return wrapper
        

        

class Product:

 
    def __init__(self,p_name='',price=''):
        self.p_name = p_name;
        self.price = price;
    

    @processJsonFileDecorator(shouldFileUpdate=False)
    def getProducts(self,response):
        if response['products']:
           return response['products']
        else:
            print('Product Not Found')
            return []

    @abstractmethod
    def getProductByID(self):
        pass


    @processJsonFileDecorator
    def getProductPriceByID(self,response,id):
        userDetails = next((product for product in response["products"] if product['id']==id),None)
        if userDetails:
            return userDetails['price']
        else:
            print('Product not found Price')
            return False



        

    def checkProductIdExist(self,productID):
        products = self.getProducts()
        isProductExist =  next((item for item in products if item["id"]==productID),None)
        if isProductExist:
            return True
        else:
            return False

        
          

    
    @processJsonFileDecorator()
    def  save(self,response):
        try:
            if self.p_name and self.price:
                data = {
                    "id" : 0,
                    "p_name":self.p_name,
                    "price":int(self.price)
                }
                
                counter = len(response["products"])
                if counter>=1:
                    data["id"] = counter+1
                else:
                    data["id"] = 1
                response["products"].append(data)
                print("Product saved successfully !!")
                return response
            else:
                print("Empty Parameters !! Initialized Product object with it's Property")
                return False
        except:
            print("Failed to Saved !!")
            return False


        
  

 


class User:

    def __init__(self,username,password):
        self.username = username;
        self.password = password;
        self.isPremium = 0;
        self.isAdmin = 0;

    def makePremium(self):
        self.isPremium = 1
        return self.User
    


    @processJsonFileDecorator
    def save_user(self,response):

        try:
            newUser = {
                'id':0,
                'username':self.username,
                'password':self.password,
                'isPremium':self.isPremium,
                'isAdmin':self.isAdmin
            }
            
            userList = response["users"]
            for i in userList:
                    if i['username'] == self.username:
                        print('User already exist !!')
                        return False
                        
                    
            
            userID = len(userList)+1
            newUser['id'] = userID
            userList.append(newUser)
            return True
            
        except:
            print("Failed to saved user")
            return False
            
        



class ShoppingCart(Product):
    def __init__(self, username):
        self.username = username


    @processJsonFileDecorator(shouldFileUpdate=False)
    def getCartDetails(self,response):
        userDetails = next((product for product in response["carts"] if product['username']==self.username),None)
        if userDetails['cartDetails']:
            return userDetails['cartDetails']
        else:
            return []


    def getProductByID(self,p_id):
        products = next(( product  for product in self.getProducts() if product['id']==int(p_id)),None)
        if len(products)>=1:
           return products
        else:
            print("Product not found")
            return []


        
     

   # pending....
    @processJsonFileDecorator()
    def addProductToCart(self,response,p_id,quantity):
        try:
                userExisted =  next((user for user in response["carts"] if user["username"] ==  self.username),None)
                if userExisted:
                     productExist = next((product for product in userExisted['cartDetails'] if product["p_id"]==p_id),None)
                     if productExist:
                         productExist["quantity"] += quantity
                     else:
                         userExisted["cartDetails"].append({"p_id":p_id,"quantity":quantity})
                else:
                    new_cart = {"username":self.username,"cartDetails":[{"p_id":p_id,"quantity":quantity}]}
                    response["carts"].append(new_cart)
                return True
                
        except Exception as e:
             print(f"Something went wrong:{e}")
             return False
                 
    
        
    @processJsonFileDecorator
    def removeProductToCart(self,response,p_id):
        try:
                userExisted =  next((user for user in response["carts"] if user["username"] ==  self.username),None)
                if userExisted:
                    productExist = next((product for product in userExisted['cartDetails'] if product["p_id"]==p_id),None)
                    if productExist:
                        userExisted["cartDetails"].remove(productExist)
                        print("Product Removed Successfully")
                        return True
                    else:
                        print('Product not found in your cart')
                        return False
                else:
                    print("Your cart is empty !!")
                    return False

                    
        except Exception as e:
                print(f"Something went wrong:{e}")
                return False

    
    @processJsonFileDecorator(shouldFileUpdate=False)
    @discount_10_percent
    def calculateTotalCost(self,response):
        try:
            userExisted =  next((user for user in response["carts"] if user["username"] ==  self.username),None)
            if userExisted["cartDetails"]:
                productPrice = map((lambda product:self.getProductPriceByID(product['p_id'])*product['quantity']),userExisted['cartDetails'])
                total = sum(productPrice)
                return total
            else:
                print('Product not found')
                return False


        except Exception as e:
            print(f"Product Fetched error {e}")

       
    def generateInvoice(self):
         return self.calculateTotalCost()
    

def loadingEffect(msg,len,delay):
    print(msg)
    for i in range(len+1):
        percentage = (i/len)*100
        loading_bar = "_" * i + ">" + "." * (len-i)
        print(f"\r{loading_bar} {percentage:.2f}%",end='',flush=True)
        time.sleep(delay)
    print()
    return True








    

def main_code():
 

   productList = []
   choice = 0
   isAuthonicated = False
   authUser = ""
   isLoading = False
   loadingEffect('Initializing...',30,0.2)
   status = loadingEffect('Checking Database...',30,0.3)
   if status:
       file_status = checkFileExist()
       if not file_status:
          status = loadingEffect(' Essential file is being created...',30,0.2)
   isLoading = True


   
  
   if isLoading: 
        while choice != 11:
            print()
            print('******* 🛒🎁 Shopping Cart 🎁🛒 *******')
            if not isAuthonicated:
                print('1) Login')
                print('2) Signup')
            # print('3) View Cart')
            print('4) Add Product to Cart')
            print('5) Removing Products from Cart')
            print('6) Calculate the Total Cost')
            print('7) Generate an Invoice')
            print('8) Quit')
            if isAuthonicated:
                print('10) Logout')
            choice = int(input('Enter Your Options here:'))
            print()

            # Login
            if choice == 1:
                print(">>>>>> 🔒 Login 🔐 <<<<<<<<<")
                username = input("Enter your Username:")
                password  = input("Enter your Password:")
                isAuthonicated = checkAuthonication(username,password)
                if isAuthonicated:
                    authUser = username
                    print()
                    print(f"🤩 Welcome To Shopping cart 🎉{authUser}🎊")
                else:
                    print("Login Failed")
                print()

            # Signup
            elif choice == 2:
                if isAuthonicated:
                    print("You alredy authorized")
                    
                print(">>>>> Signup <<<<<<")
                username = input("Enter your Username:")
                password  = input("Enter your Password:")
                newUser =  User(username,password)
                newUser = newUser.save_user()
                if newUser:
                    print("Congratulations!!🎉 Account Created Successfully")
                    isAuthonicated = True
                    authUser = username
                else:
                    print("Something went wrong 😓")

            # Add Cart
            elif choice == 4:
                if isAuthonicated:
                    cart = ShoppingCart(authUser)
                    print(" 🏪 Welcome to Shop 🏬 ")
                    print(" 🏪 Add Your Favourate Product to Your Cart 🏬 ")
                    productObj = Product()
                    productList = productObj.getProducts()
                    print('-'*37)
                    print(f'| id  |  Product Name |    Price    | ')
                    print('-'*37)
                    for product in productList:
                        print(f'| {product["id"]}{(len("id")-len(str(product["id"])))* " "}  |  {product["p_name"]}{(len("Product Name")-len(product["p_name"]))* " "} |  Rs.{product["price"]}{(len("   price   ")-len("  Rs."+str(product["price"])))* " "}  | ')
                    print('-'*37)
                    print()
                
                    print(" 😇 Press 0 to Close your Cart 😇 ")
                    productID  = int(input("Enter the Product Id :"))
                    isProductExist = cart.checkProductIdExist(productID)
                    if isProductExist:
                        quantity = int(input("Number of Items :"))
                        newProduct = cart.addProductToCart(productID,quantity)
                        if newProduct:
                            print(" 🎉 Product Added to cart Successfully !!")
                        else:
                            print("Something went Wrong")
                    else:
                        print("Product ID doesn't Exist")

            # Remove Product
            elif choice == 5:
                if isAuthonicated:
                    cart = ShoppingCart(authUser)
                    print(" 🏪 Your Cart 🏬 ")
                    productObj = Product()
                    productList = cart.getCartDetails()
                    getProductName = lambda x: cart.getProductByID(x).get('p_name')
                    getProdcutPrice = lambda x: cart.getProductPriceByID(x)
                    if productList:
                        print('-'*49)
                        print(f'| id  |  Product Name |    Price    | Quantity  |')
                        print('-'*49)
                        for product in productList:
                            print(f'| {product["p_id"]}{(len("id")-(len(str(product["p_id"]))))* " "}  |  {getProductName(product["p_id"])}{(len("Product Name")-(len(getProductName(product["p_id"]))))* " "} | Rs.{getProdcutPrice(product["p_id"])}{(len("    price    ")-len("  Rs."+str(getProdcutPrice(product["p_id"]))))* " "} | {product["quantity"]}{(len("Quantity")-(len(str(product["quantity"]))))* " "}  | ')
                        print('-'*49)
                        print()
                        print("Remove products from cart using Product 'id'")
                        print("Press 0 to cancel")
                        productID  = int(input("Enter the Product Id :"))
                        isProductExist = cart.checkProductIdExist(productID)
                        if isProductExist:
                            newProduct = cart.removeProductToCart(productID)
                            if newProduct:
                                print(" 🎉 Product Removed Successfully !!")
                            else:
                                print("Something went Wrong")
                        else:
                            print("Product ID doesn't Exist")

                else:
                    print("🚀  Please Login first !!")
                    print("⚠️  You are not Authorized ⚠️")

            elif choice == 6:
                if isAuthonicated:
                    cart = ShoppingCart(authUser)
                    total_price = cart.calculateTotalCost()['total_cost']
                    if total_price:
                        print(f"Your total cost is Rs.{total_price}")
                    else:
                        print("Your cart is empty")
                else:
                    print(" Please Login first !!")

            # Generate Invoice
            elif choice == 7:
                if isAuthonicated:
                    cart = ShoppingCart(authUser)
                    print("Invoice")
                    productObj = Product()
                    productList = cart.getCartDetails()
                    getProductName = lambda x: cart.getProductByID(x).get('p_name')
                    getProdcutPrice = lambda x: cart.getProductPriceByID(x)
                    getFinalPrice = lambda quantity,ID: quantity * getProdcutPrice(ID) 
                    invoiceDetails = cart.generateInvoice()
                    if invoiceDetails:
                        isUserPremium = 'Premium' if invoiceDetails['userType'] else 'Normal'
                        print('-'*62)
                        template_User = f" User : {invoiceDetails['username']}({isUserPremium}) |"
                        print(f"|{(62-(1+len(template_User)))*' '}{template_User}")

                        print('-'*62)
                        print(f'| id  |  Product Name |    Price    | Quantity | Final Price |')
                        print('-'*62)
                        for product in productList:
                            print(f'| {product["p_id"]}{(len("id")-(len(str(product["p_id"]))))* " "}  |  {getProductName(product["p_id"])}{(len("Product Name")-(len(getProductName(product["p_id"]))))* " "} | Rs.{getProdcutPrice(product["p_id"])}{(len("    price    ")-(5+len(str(getProdcutPrice(product["p_id"])))))* " "} | {product["quantity"]}{(len("Quantity")-(1+len(str(product["quantity"]))))* " "}  | Rs.{getFinalPrice(product["quantity"],product["p_id"])}{(len("Final Price")-(4+len(str(getFinalPrice(product["quantity"],product["p_id"])))))* " "}  | ')
                        print('-'*62)
                        templat_orginalPrice =  f" Orginal Price : {invoiceDetails['discount_Price']+invoiceDetails['total_cost']} |"
                        template_DiscountApplied = f" Discount Applied : {'10%' if invoiceDetails['userType'] else '0.0'} |"
                        template_DiscountPrice = f" Discount Price : {invoiceDetails['discount_Price']} |"
                        template_totalCost = f" Total Cost : {invoiceDetails['total_cost']} |"
                
                        print(f"|{(62-(1+len(templat_orginalPrice)))*' '}{templat_orginalPrice}")
                        print(f"|{(62-(1+len(template_DiscountApplied)))*' '}{template_DiscountApplied}")
                        print(f"|{(62-(1+len(template_DiscountPrice)))*' '}{template_DiscountPrice}")
                        print('-'*62)
                        print(f"|{(62-(1+len(template_totalCost)))*' '}{template_totalCost}")
                        print('-'*62)
                        print()
                    else:
                        print("Your Cart is empty")
                    

                else:
                    print("🚀  Please Login first !!")
                    print("⚠️  You are not Authorized ⚠️")

            
                
    
            elif choice == 8:
                    return
            # Logout
            elif choice == 9:
                    isAuthonicated = False
                    authUser = ''
                    print("Logout Successfull 👋")
            
            #other
            else:
                print("Invalid Options 😓")

            
        

          
            
            

def test_code():
    response = {}
    obj = ShoppingCart('nischal')
    # obj = Product('Iphone','100000')
    product = obj.getProductByID(1)
    print(product)



if __name__ == "__main__":
    main_code()
    # test_code()
    

        
      
 