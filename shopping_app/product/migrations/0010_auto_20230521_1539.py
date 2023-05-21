# Generated by Django 3.2.7 on 2023-05-21 12:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0009_auto_20230501_1708'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductSpecification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('attribute', models.CharField(max_length=255, verbose_name='ویژگی')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='product.category', verbose_name='دسته بندی')),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpecificationValue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=255, verbose_name='مقدار')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='design',
        ),
        migrations.DeleteModel(
            name='Design',
        ),
        migrations.AddField(
            model_name='productspecificationvalue',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='product.product', verbose_name='محصول'),
        ),
        migrations.AddField(
            model_name='productspecificationvalue',
            name='specification',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product.productspecification', verbose_name='ویژگی'),
        ),
    ]
