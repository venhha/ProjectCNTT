from django.contrib import admin
from .models import Author, Product, Category, Books

# Register your models here.
admin.site.register(Author)
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Books)