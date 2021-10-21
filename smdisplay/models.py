

from django.db import models
from django.contrib.auth.models import User


PRODUCT_CHOICES= (
    ('Mag', "Magnetic"),('NM', "NonMagnetic"), 
    ('Sign', "Signage"), ('stand', "Stand"),
)

class Customer(models.Model):
    user= models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name= models.CharField(max_length=200, null=True)
    email= models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name  # this is goig to be the value which shows up in our admin panel when we create our model Customer


class Product(models.Model):
    name= models.CharField(max_length=200, null=True)
    price= models.FloatField()
    digital= models.BooleanField(default=False, null=True, blank=True)
    description= models.TextField(default="Description")
    category= models.CharField(choices= PRODUCT_CHOICES, max_length=20, null=True)
    image= models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
    
    # CREATE A MODEL-METHOD for the 'image' field.. to try-handle exception arising out of lack of image
    # So if some image is not available, then the code doesn't crash & page renders properly
    # Instead of calling the image-url directly(ex- productxyz_image.url).. we want to use a MODEL METHOD
    # MODEL METHOD would either render an image or a text depending upon availability of the image
    # add a MODEL METHOD into the Product class. Use @property decorator to access it like an attribute
    # Inside the MODEL METHOD.. use try-except block to handle any exception
    
    @property
    def imageURL(self):
        try:
            url = self.image.url  # if image url is available in the instance
        except:
            url= " " # if url not available, just add a " " to the 'url'
        
        return url
        


class Order(models.Model):   # Order represents the "cart"
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered= models.DateTimeField(auto_now_add=True)
    complete= models.BooleanField(default=False)
    transaction_id= models.CharField(max_length=100, null=True)

    def __str__(self):
        return str(self.id)
    
    # First get the total value of all the items in the order cart
    # Second, get the total quantity of all the items in the order cart

    @property
    def cartTOTAL(self):
        cart_items= self.orderitem_set.all()
        total_value = sum([item.itemTOTAL for item in cart_items])
        return total_value
    
    @property
    def cartQUANTITY(self):
        cart_items= self.orderitem_set.all()
        cart_quantity= sum([item.quantity for item in cart_items])
        return cart_quantity


class OrderItem(models.Model):   # OrderItem represents each "item" within the cart
    product= models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity= models.IntegerField(default=0, null=True, blank=True)
    date_added= models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return str(self.id)
    
    @property
    def itemTOTAL(self):
        total= self.product.price * self.quantity
        return total
    
    '''@property
    def cartTOTAL(self):
        cart_total='''




class ShippingAddress(models.Model):
    customer= models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order= models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address= models.CharField(max_length=100, null=False)
    city= models.CharField(max_length=100, null=False)
    state= models.CharField(max_length=100, null=False)
    zipcode= models.CharField(max_length=50, null=False)
    date_added= models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.address


  
    