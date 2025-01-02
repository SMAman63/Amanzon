# Generated by Django 5.1.4 on 2024-12-25 09:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_alter_category_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='is_sale',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='product',
            name='sale_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=6),
        ),
    ]