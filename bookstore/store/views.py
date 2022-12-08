from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect,  JsonResponse
import json

#from django.template import loader
#from django.urls import reverse
# Create your views here.
from .models import *
from .forms import RegistrationForm


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    return render(request, 'store/register.html', {'form': form})


def store(request):
    books = Product.objects.all()
    context = {'books': books}
    return render(request, 'store/store.html', context)


def cart(request):

    orders = Order.objects.filter(iID=4)
        
    total_items = sum([i.quantity for i in orders])
    total_price = '{:,}'.format(sum([i.get_total for i in orders]))
    
    context = {'orders': orders, 'total_items': total_items,
               'total_price': total_price}

    return render(request, 'store/cart.html', context)


def checkout(request):
    orders = Order.objects.filter(iID=3)
    total_items = sum([i.quantity for i in orders])
    total_price = '{:,}'.format(sum([i.get_total for i in orders]))
    
    context = {'orders': orders, 'total_items': total_items,
               'total_price': total_price}

    return render(request, 'store/checkout.html', context)

def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']
    
    print('productID: ', productID)
    print('Action: ', action)
    
    customer = request.user.customer
    product = Product.objects.get(pID=productID)
    
    invoice, created = Invoice.objects.get_or_create(cusID=customer)
    orderItem, created = Order.objects.get_or_create(iID=invoice, pID=product)
    
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)
'''
def index(request):
    books = Books.objects.all().values()
    return render(request, 'pages/index.html', context={'books': books})


def add(request):
    template = loader.get_template('pages/add.html')
    return HttpResponse(template.render({}, request))


def addrecord(request):
    n = request.POST['book_name']
    book = Books()
    book.book_name = n
    book.save()
    return HttpResponseRedirect(reverse('pages/index'))


def delete(request, id):
    book = Books.objects.get(id=id)
    book.delete()
    return HttpResponseRedirect(reverse('pages/index'))


def update(request, id):
    book = Books.objects.get(id=id)
    return render(request, 'pages/update.html', context={'book': book})


def updaterecord(request, id):
    name = request.POST['name']
    num = request.POST['num']
    book = Books.objects.get(id=id)
    book.book_name = name
    book.stock_num = num
    book.save()
    return HttpResponseRedirect(reverse('pages/index'))
'''
