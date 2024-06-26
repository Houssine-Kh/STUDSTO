# Generated by Django 5.0.1 on 2024-01-16 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('products', '0004_alter_productimage_table'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='shared_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='shared_products', to='accounts.userprofile'),
        ),
    ]
