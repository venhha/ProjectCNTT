from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse

from .models import Books
# Create your views here.


def index(request):
    books = Books.objects.all().values()
    return render(request, 'index.html', context={'books': books})


def add(request):
    template = loader.get_template('add.html')
    return HttpResponse(template.render({}, request))


def addrecord(request):
    n = request.POST['book_name']
    book = Books()
    book.book_name = n
    book.save()
    return HttpResponseRedirect(reverse('index'))


def delete(request, id):
    book = Books.objects.get(id=id)
    book.delete()
    return HttpResponseRedirect(reverse('index'))


def update(request, id):
    book = Books.objects.get(id=id)
    return render(request, 'update.html', context={'book': book})


def updaterecord(request, id):
    name = request.POST['name']
    num = request.POST['num']
    book = Books.objects.get(id=id)
    book.book_name = name
    book.stock_num = num
    book.save()
    return HttpResponseRedirect(reverse('index'))


def testing(request):
    mybooks = Books.objects.all()
    template = loader.get_template('t.html')
    context = {
        'mybooks': mybooks,
    }
    return HttpResponse(template.render(context, request))
