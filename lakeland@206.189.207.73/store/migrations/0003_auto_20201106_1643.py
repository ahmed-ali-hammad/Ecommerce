# Generated by Django 3.1.2 on 2020-11-06 21:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='images/product.png', upload_to=''),
        ),
    ]
