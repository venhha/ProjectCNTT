from django.shortcuts import render
from django.http import HttpResponse
from .models import Books

# Create your views here.
def index(request):
    #return render(request, 'index.html')
    books = Books.objects.all().values()
    output = ""
    for x in books:
        output += x["book_name"]+','
    return HttpResponse(output)