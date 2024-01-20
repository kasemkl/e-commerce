from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
# Create your views here.
def store(request):
    products=Product.objects.all()
    context={'products':products}
    return render(request,'store/store.html',context) 

def cart(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else :
        items=[]
        order=[]
    context={'items':items,'order':order}
    return render(request,'store/cart.html',context) 
def checkout(request):
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        items=order.orderitem_set.all()
    else :
        items=[]
        order=[]
    context={'items':items,'order':order}
    return render(request,'store/checkout.html',context) 

def UpdateItem(request):
    data=json.loads(request.body)
    productId=data['productId']
    action=data['action']
    print('productId:' + str(productId) + '  action:'+str(action) )
    
    customer=request.user.customer
    product=Product.objects.get(id=productId)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)
    
    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)
    
    if action=='add':
        orderItem.quantity=orderItem.quantity+1
    elif action=='remove':
        orderItem.quantity=orderItem.quantity - 1
    orderItem.save()
    if orderItem.quantity<=0 :
        orderItem.delete()
        
    return JsonResponse('item was added',safe=False)

def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)
    
    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)
        order.transaction_id=transaction_id
        order.complete=True
        order.save()
        
        
    ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            )
        
    return JsonResponse('payment was submited',safe=False)