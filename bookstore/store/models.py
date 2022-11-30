from django.db import models

# Create your models here.
class Books(models.Model):
  book_name = models.CharField(max_length=255, null=True)
  stock_num = models.IntegerField(default=0, null=False)
  in_stock = models.BooleanField(default=False, null=False)