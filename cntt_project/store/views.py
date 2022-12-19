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
        
    if request.method == 'POST':
        try:
            catID = request.POST['catID']   
            products = Product.objects.filter(catID=catID)
            cates = Category.objects.all()
            context = {
                'products': products,
                'invoice': invoice,
                'cates':cates,
                'choose': Category.objects.get(catID=catID).cat_name
            }
            return render(request, 'home/index.html', context)
        except:
            products = Product.objects.all()
            cates = Category.objects.all()
            context = {
                'products': products,
                'invoice': invoice,
                'cates':cates,
            }
            return render(request, 'home/index.html', context)
    
    products = Product.objects.all()
    cates = Category.objects.all()
    context = {
        'products': products,
        'invoice': invoice,
        'cates':cates,
        }
    return render(request, 'home/index.html', context)


def index_search(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        invoice, created = Invoice.objects.get_or_create(
            cusID=customer, place_status=False)
    else:
        # when user not login
        invoice = {'get_total_item': 0, 'get_total_price': 0}
    
    try:
        query = request.POST['search_query']
    except:
        query = ""
        
    products = Product.objects.filter(book_name__icontains = query)
    cates = Category.objects.all()
    context = {
        'products': products,
        'invoice': invoice,
        'cates':cates,
        }
    return render(request, 'home/index.html', context)

def error_404_view(request, exception):
    return render(request, 'pages/404.html', {'message': exception})


def product_detail_view(request, pID):
    if request.user.is_authenticated:
        customer = request.user.customer
        invoice, created = Invoice.objects.get_or_create(
            cusID=customer, place_status=False)
    else:
        # when user not login
        invoice = {'get_total_item': 0, 'get_total_price': 0}

    p = Product.objects.get(pID=pID)
    context = {'p': p,}
    return render(request, 'home/product/product_detail.html', context)


def author_detail_view(request, auID):
    if request.user.is_authenticated:
        customer = request.user.customer
        invoice, created = Invoice.objects.get_or_create(
            cusID=customer, place_status=False)
    else:
        # when user not login
        invoice = {'get_total_item': 0, 'get_total_price': 0}

    author = Author.objects.get(auID=auID)
    list_product = list(author.get_list_product)

    context = {'author': author,
               'list_product': list_product, 'invoice': invoice, }
    return render(request, 'home/author/author_detail.html', context)


def register(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Tạo người dùng thành công!')
            return HttpResponseRedirect('/')
    return render(request, 'home/accounts/register.html', {'form': form})


def edit_profile(request):

    if request.method == 'POST':
        try:
            cus = Customer.objects.get(user=request.user)
            cus.cus_name = request.POST['cus_name']
            cus.cus_addr = request.POST['cus_addr']
            cus.cus_phone = request.POST['cus_phone']
            cus.save()
            return render(request, 'home/accounts/edit_profile.html', {'cus': cus})
        except:
            return HttpResponse("Lỗi chỉnh sửa")

    # request get
    cus = Customer.objects.get(user=request.user)
    context = {'cus': cus}
    return render(request, 'home/accounts/edit_profile.html', context)


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


def add_to_cart(request):
    if request.user.is_authenticated:
        try:
            pID = request.POST['pID']
            quantity = request.POST['quantity']
            customer = request.user.customer

            product = Product.objects.get(pID=pID)
            invoice, created = Invoice.objects.get_or_create(
                cusID=customer, place_status=False)
            order, created = Order.objects.get_or_create(
                iID=invoice, pID=product)

            order.quantity = order.quantity + int(quantity)
            order.save()

            all_product_list = Product.objects.all()
            context = {'books': all_product_list, 'invoice': invoice}
            return render(request, 'home/index.html', context)
        except:
            print("ERROR add_to_cart")
            pass
    return HttpResponse("Lỗi")


def updateItem(request):
    data = json.loads(request.body)
    productID = data['productID']
    action = data['action']

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


def checkout_submit(request):
    iID = request.POST['iID']
    ship_addr = request.POST['ship_addr']

    try:
        i = Invoice.objects.get(iID=iID)
        i.ship_addr = ship_addr
        i.date_checkout = datetime.now()
        i.place_status = True
        i.save()

        invoice = Invoice.objects.filter(
            cusID=request.user.customer, place_status=True)
        context = {'invoice': invoice}
        return render(request, 'home/checkout/checkout_info.html', context)
    except:
        return HttpResponse("Đặt hàng không thành công")


def checkout_info_view(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        invoice = Invoice.objects.filter(cusID=customer, place_status=True)
        #orders = invoice.order_set.all()
    else:
        # when user not login
        invoice = {'get_total_item': 0, 'get_total_price': 0}

    context = {'invoice': invoice}
    return render(request, 'home/checkout/checkout_info.html', context)


def view_checkout_detail(request, iID):
    invoice = Invoice.objects.get(iID=iID)
    orders = invoice.order_set.all()
    context = {'invoice': invoice, 'orders': orders, }
    return render(request, 'home/checkout/checkout_detail.html', context)


def order_comment(request, oID):
    if request.method == 'POST':
        try:
            order = Order.objects.get(oID=oID)
            order.comment = request.POST['cmt']
            order.save()
            
            invoice = Invoice.objects.get(iID=order.iID.iID)
            orders = invoice.order_set.all()
            context = {'invoice': invoice, 'orders': orders, }
            return render(request, 'home/checkout/checkout_detail.html', context)
        except:
            return HttpResponse("Lỗi bình luận")

'''
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

"""def placeOrder(request):
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

if request.user.is_authenticated:
    customer = request.user.customer
    invoice = Invoice.objects.get(cusID=customer)
    orders = invoice.order_set.all()
    print('yeye: ',invoice.iID)
else:
    # when user not login
    invoice = {'get_total_item': 0, 'get_total_price': 0}
    orders = []

ship_addr = request.POST["ship_addr"]
customer = request.user.customer
print(ship_addr)
print(customer)
"""
