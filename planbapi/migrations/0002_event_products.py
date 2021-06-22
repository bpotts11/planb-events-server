# Generated by Django 3.2.4 on 2021-06-21 18:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planbapi', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='products',
            field=models.ManyToManyField(related_name='products', through='planbapi.EventProduct', to='planbapi.Product'),
        ),
    ]
