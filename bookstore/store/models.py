from django.db import models

# Create your models here.


class Books(models.Model):
    book_name = models.CharField(max_length=255, null=True)
    stock_num = models.IntegerField(default=0, null=False)
    in_stock = models.BooleanField(default=False, null=False)
    
    def get_absolute_url(self):
        print(self)
        #print("123")
        return reverse("books_detail", kwargs={"pk": self.pk})
        #return '/%s/' % self.id

class Author(models.Model):

    auID = models.AutoField(primary_key=True)
    au_name = models.CharField(max_length=50)
    au_star = models.FloatField(default=0)
    
    def __str__(self):
        return self.au_name

    def get_absolute_url(self):
        return reverse("author_detail", kwargs={"pk": self.pk})

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
    auID = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    catID = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    book_price = models.IntegerField(default=0, null=False)
    book_stock = models.IntegerField(default=0, null=False)
    book_star = models.FloatField(null=True)
    book_description = models.CharField(max_length=254, null=True)
    
    def __str__(self):
        return self.book_name

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"pk": self.pk})