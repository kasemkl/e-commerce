from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank=True)
    name=models.CharField(max_length=200,null=True)
    email=models.EmailField(null=True)
    
    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    name=models.CharField(max_length=200,null=True)
    price=models.DecimalField(max_digits=6,decimal_places=2)
    digital=models.BooleanField(null=True,blank=False,default=False)
    image=models.ImageField(null=True,blank=True)
    def __str__(self) -> str:
        return self.name
    @property
    def imageURL(self):
        try:
            url=self.image.url
        except:
            url='/images/placeholder.png'
        return url
    
class Order(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    date_ordered=models.DateTimeField(auto_now_add=True)
    complete=models.BooleanField(default=False,blank=False,null=True)
    transaction_id=models.CharField(max_length=200,null=True)
    
    def __str__(self) -> str:
        return str(self.id)
    
    def total_price(self):
        return sum([item.total() for item in self.orderitem_set.all()])
    def shipping(self):
        shipping = False 
        orderItems=self.orderitem_set.all()
        for item in orderItems:
            if item.product.digital==False:
                shipping=True
                break
        return shipping
class OrderItem(models.Model):
    product=models.ForeignKey(Product,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    quantity=models.IntegerField(default=0,blank=True,null=True)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.product.name
    def total(self):
        return self.quantity*self.product.price
        
class ShippingAddress(models.Model):
    customer=models.ForeignKey(Customer,on_delete=models.SET_NULL,blank=True,null=True)
    order=models.ForeignKey(Order,on_delete=models.SET_NULL,blank=True,null=True)
    address=models.CharField(max_length=200,null=False)
    city=models.CharField(max_length=200,null=False)
    state=models.CharField(max_length=200,null=False)
    zipcode=models.CharField(max_length=200,null=False)
    date_added=models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.address
    