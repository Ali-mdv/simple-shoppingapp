# Generated by Django 3.2.7 on 2023-05-23 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('static_data', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='siteinfo',
            name='instagram_link',
            field=models.URLField(blank=True, null=True, verbose_name='آدرس اینستاگرام'),
        ),
        migrations.AddField(
            model_name='siteinfo',
            name='telegram_link',
            field=models.URLField(blank=True, null=True, verbose_name='آدرس تلگرام'),
        ),
        migrations.AddField(
            model_name='siteinfo',
            name='whatsapp_link',
            field=models.URLField(blank=True, null=True, verbose_name='آدرس واتساپ'),
        ),
    ]