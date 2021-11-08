# Generated by Django 3.2.7 on 2021-11-08 15:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('smdisplay', '0004_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='product',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=7),
        ),
    ]
