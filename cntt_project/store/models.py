from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.


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
    book_description = models.TextField(null=True)

    def __str__(self):
        return str(self.pID)

    def get_absolute_url(self):
        # return f'/{self.slug}'
        return reverse("store:product_detail", kwargs={"pID": self.pk})

    @property
    def get_author(self):
        author_list = list(self.author_set.all())
        return author_list

    @property
    def get_imgURL(self):
        try:
            url = self.book_img.url
        except:
            url = ''
        return url


class Author(models.Model):

    auID = models.AutoField(primary_key=True)
    pID = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    au_name = models.CharField(max_length=50)
    au_star = models.FloatField(default=0)

    def __str__(self):
        return self.au_name

    def get_absolute_url(self):
        return reverse("store:author_detail", kwargs={"auID": self.pk})
    
    @property
    def get_list_product(self):
        print("HEKEHKJEFEKJBFKJ")
        list = Author.objects.filter(auID=self.auID)
        return list

class Customer(models.Model):
    cusID = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        User, null=True, blank=True, on_delete=models.CASCADE)
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
    # date create
    date = models.DateField(auto_now=False, auto_now_add=True, null=True)
    # checkout info
    date_checkout = models.DateField(
        null=True, auto_now=False, auto_now_add=False)
    place_status = models.BooleanField(
        null=True, default=False)  # đã đặt hàng chưa? 0: chưa đặt
    # giao chưa? 0: giao chưa đến
    status = models.BooleanField(null=True, default=False)
    ship_addr = models.CharField(null=True, max_length=254)

    def __str__(self):
        return str(self.iID)

    def get_absolute_url(self):
        return reverse("store:checkout_detail", kwargs={"iID": self.pk})

    @property
    def get_cus_name(self):
        return self.cusID.cus_name

    @property
    def get_date_checkout(self):
        return self.date_checkout

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
    # danh gia sp cua khach da mua hang
    comment = models.TextField(null=True)

    @property
    def get_total(self):
        total = self.pID.book_price * self.quantity
        return total

    def __str__(self):
        return self.oID

    def get_absolute_url(self):
        return reverse("oder_detail", kwargs={"pk": self.pk})
