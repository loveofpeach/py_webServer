# Generated by Django 4.2 on 2024-10-13 16:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0003_bookinfo_bcomment_bookinfo_bread_bookinfo_isdelete_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookinfo',
            name='bprice',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]