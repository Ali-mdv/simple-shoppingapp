# Generated by Django 3.2.7 on 2023-05-21 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0010_auto_20230521_1539'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='body_color',
        ),
        migrations.RemoveField(
            model_name='product',
            name='description',
        ),
        migrations.AddField(
            model_name='product',
            name='color',
            field=models.ManyToManyField(to='product.Color', verbose_name='رنگ'),
        ),
        migrations.AddField(
            model_name='product',
            name='dimensions',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='ابعاد'),
        ),
        migrations.AddField(
            model_name='product',
            name='introduction',
            field=models.TextField(default=1, verbose_name='معرفی اجمالی'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='product',
            name='other_description',
            field=models.TextField(blank=True, max_length=500, null=True, verbose_name='توضیحات دیگر'),
        ),
        migrations.AddField(
            model_name='product',
            name='weight',
            field=models.DecimalField(blank=True, decimal_places=1, max_digits=5, null=True, verbose_name='وزن'),
        ),
    ]
