from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
import json
from datetime import datetime
#from django.template import loader
#from django.urls import reverse
# Create your views here.
from .models import *
from .forms import RegistrationForm


def index(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        invoice, created = Invoice.objects.get_or_create(
            cusID=customer, place_status=False)
    else:
        # when user not login
        invoice = {'get_total_item': 0, 'get_total_price': 0}

    books = Product.objects.all()
    context = {'books': books, 'invoice': invoice}
    return render(request, 'home/index.html', context)

def error_404_view(request, exception):
    return render(request, 'pages/404.html', {'message': exception})

def book_detail_view(request, pID):
    p = Product.objects.get(pID=pID)
    orders = Order.objects.filter(pID=pID)
    context = {'p': p, 'orders': orders}
    return render(request, 'home/product/product_detail.html', context)


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            cus_name = request.POST["cus_name"]
            cus_addr = request.POST["cus_addr"]
            cus_phone = request.POST["cus_phone"]
            cus = Customer.objects.create(
                user=new_user, cus_name=cus_name, cus_addr=cus_addr, cus_phone=cus_phone)
            print(new_user.username)
            print(cus.cus_name)

            return HttpResponseRedirect('/')
    return render(request, 'home/accounts/register.html', {'form': form})


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        invoice, created = Invoice.objects.get_or_create(
            cusID=customer, place_status=False)
        orders = invoice.order_set.all()
    else:
        # when user not login
        invoice = {'get_total_item': 0, 'get_total_price': 0}
        orders = []

    context = {'orders': orders, 'invoice': invoice}
    return render(request, 'home/cart/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        invoice, created = Invoice.objects.get_or_create(
            cusID=customer, place_status=False)
        orders = invoice.order_set.all()
    else:
        # when user not login
        invoice = {'get_total_item': 0, 'get_total_price': 0}
        orders = []

    context = {'orders': orders, 'invoice': invoice}
    return render(request, 'home/checkout/checkout.html', context)


def placeOrder(request):
    data = json.loads(request.body)
    addr = data['addr']
    action = data['action']
    iID = data['iID']

    print('ship_addr: ', addr)
    print('action: ', action)
    print('iID: ', iID)

    invoice = Invoice.objects.get(iID=iID)
    invoice.date_checkout = datetime.now()
    invoice.place_status = True
    invoice.ship_addr = addr
    invoice.save()

    return JsonResponse('Đã đặt hàng', safe=False)

    '''if request.user.is_authenticated:
        customer = request.user.customer
        invoice = Invoice.objects.get(cusID=customer)
        orders = invoice.order_set.all()
        print('yeye: ',invoice.iID)
    else:
        # when user not login
        invoice = {'get_total_item': 0, 'get_total_price': 0}
        orders = []'''

    '''ship_addr = request.POST["ship_addr"]
    customer = request.user.customer
    print(ship_addr)
    print(customer)'''


def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

    print('productID: ', productID)
    print('Action: ', action)
    #print("updateItem- view.py")
    customer = request.user.customer
    product = Product.objects.get(pID=productID)

    invoice, created = Invoice.objects.get_or_create(
        cusID=customer, place_status=False)
    orderItem, created = Order.objects.get_or_create(iID=invoice, pID=product)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    elif action == 'delete':
        orderItem.quantity = 0
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
    return JsonResponse('Item was added', safe=False)


def checkout_info_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        invoice = Invoice.objects.filter(cusID=customer, place_status=True)
        #orders = invoice.order_set.all()
    else:
        # when user not login
        invoice = {'get_total_item': 0, 'get_total_price': 0}
        orders = []

        # 'orders': orders,
    context = {'invoice': invoice}
    return render(request, 'home/checkout/checkout_info.html', context)


def view_checkout_detail(request, iID):
    invoice = Invoice.objects.get(iID=iID)
    orders = invoice.order_set.all()
    context = {'invoice': invoice, 'orders': orders, }
    return render(request, 'home/checkout/checkout_detail.html', context)


def comment(request):
    data = json.loads(request.body)
    text = data['text']
    action = data['action']
    oID = data['oID']

    print('text: ', text)
    print('action: ', action)
    print('oID: ', oID)

    order = Order.objects.get(oID=oID)
    order.comment = text
    order.save()

    return JsonResponse('Đã ghi nhận đánh giá thành công', safe=False)


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
