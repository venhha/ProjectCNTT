from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ['oID', 'quantity', 'pID']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['pID', 'book_name', ]
    list_filter = ['pID','book_name',]
    search_fields = ['book_name']
    
class CateAdmin(admin.ModelAdmin):
    list_display = ['catID', 'cat_name', ] 
    
    
    
# Register your models here.
admin.site.register(Author)
admin.site.register(Category, CateAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Invoice)
admin.site.register(Customer)
