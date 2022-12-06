from django.contrib import admin
from .models import *

class OrderAdmin(admin.ModelAdmin):
    list_display = ['oID', 'pID', 'iID']

# Register your models here.
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Product)

admin.site.register(Order, OrderAdmin)
admin.site.register(Invoice)
admin.site.register(Customer)
