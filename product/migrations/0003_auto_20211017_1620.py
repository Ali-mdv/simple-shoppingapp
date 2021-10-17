# Generated by Django 3.2.7 on 2021-10-17 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_auto_20210926_1732'),
    ]

    operations = [
        migrations.CreateModel(
            name='IPAdrees',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip_address', models.GenericIPAddressField(verbose_name='آی پی آدرس')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='hits',
            field=models.ManyToManyField(blank=True, to='product.IPAdrees', verbose_name='بازدید'),
        ),
    ]
