from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Books(models.Model):
    book_name = models.CharField(max_length=255, null=True)
    stock_num = models.IntegerField(default=0, null=False)
    in_stock = models.BooleanField(default=False, null=False)

    def get_absolute_url(self):
        print(self)
        # print("123")
        return reverse("books_detail", kwargs={"pk": self.pk})
        # return '/%s/' % self.id


class Category(models.Model):

    catID = models.AutoField(primary_key=True)
    cat_name = models.CharField(max_length=50)

    def __str__(self):
        return self.cat_name

    def get_absolute_url(self):
        return reverse("category_detail", kwargs={"pk": self.pk})


class Product(models.Model):
    pID = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=50)
    catID = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    book_img = models.ImageField(
        upload_to='uploads/', height_field=None, width_field=None, max_length=None, null=True,  blank=True)
    book_price = models.IntegerField(default=0, null=False)
    book_stock = models.IntegerField(default=0, null=False)
    book_star = models.FloatField(null=True)
    book_description = models.CharField(max_length=254, null=True)

    def __str__(self):
        return str(self.pID)

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})


class Author(models.Model):

    auID = models.AutoField(primary_key=True)
    pID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    au_name = models.CharField(max_length=50)
    au_star = models.FloatField(default=0)

    def __str__(self):
        return self.au_name

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"pk": self.pk})


class Customer(models.Model):
    cusID = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, null=True, blank=True, on_delete = models.CASCADE)
    cus_name = models.CharField(max_length=50)
    cus_addr = models.CharField(max_length=50)
    cus_phone = models.CharField(max_length=12)

    def __str__(self):
        return self.cus_name

    def get_absolute_url(self):
        return reverse("customer_detail", kwargs={"pk": self.pk})

class Invoice(models.Model):
    iID = models.AutoField(primary_key=True)
    cusID = models.ForeignKey(Customer, on_delete=models.CASCADE, null=False)
    date = models.DateField(auto_now=False, auto_now_add=True, null=True) #date create
    #checkout info
    date_checkout = models.DateField(null=True, auto_now=False, auto_now_add=False)
    place_status = models.BooleanField(null=True, default=False) #đã đặt hàng chưa? 0: chưa đặt
    status = models.BooleanField(null=True, default=False) #giao chưa? 0: giao chưa đến
    ship_addr = models.CharField(null=True,max_length=254)
    
    def __str__(self):
        return str(self.iID)

    def get_absolute_url(self):
        return reverse("invoice_detail", kwargs={"pk": self.pk})
    
    @property
    def get_total_item(self):
        orders = self.order_set.all()
        total = sum([i.quantity for i in orders])
        return total
    @property
    def get_total_price(self):
        orders = self.order_set.all()
        total = sum([i.get_total for i in orders])
        return total
    
class Order(models.Model):
    oID = models.AutoField(primary_key=True)
    pID = models.ForeignKey(Product, on_delete=models.CASCADE, null=False)
    iID = models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(null=False, default=0)

    @property
    def get_total(self):
        total = self.pID.book_price * self.quantity
        return total

    def __str__(self):
        return self.oID

    def get_absolute_url(self):
        return reverse("oder_detail", kwargs={"pk": self.pk})
