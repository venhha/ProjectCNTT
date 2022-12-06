from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
#from django.template import loader
from django.urls import reverse
from store.models import *
# Create your views here.
    
def store(request):
    books = Product.objects.all()
    context = {'books':books}
    return render(request, 'store/store.html', context)


def cart(request):
    orders = Order.objects.all()
    context = {'orders':orders}
    return render(request, 'store/cart.html', context)


def checkout(request):
    context = {}
    return render(request, 'store/checkout.html', context)


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
