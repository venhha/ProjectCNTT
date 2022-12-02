# Generated by Django 4.1.3 on 2022-12-02 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0003_author_category_product'),
    ]

    operations = [
        migrations.AlterField(
            model_name='author',
            name='au_star',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='book_description',
            field=models.CharField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='book_price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='product',
            name='book_star',
            field=models.FloatField(null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='book_stock',
            field=models.IntegerField(default=0),
        ),
    ]
