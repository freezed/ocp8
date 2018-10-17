# Generated by Django 2.1.1 on 2018-10-16 22:34

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('ersatz', '0002_auto_20181016_1755'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.RemoveField(
            model_name='product',
            name='user',
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ManyToManyField(related_name='products', to='ersatz.Category'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='products',
            field=models.ManyToManyField(related_name='favorite_products', to='ersatz.Product'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='substitutes',
            field=models.ManyToManyField(related_name='favorite_substitutes', to='ersatz.Product'),
        ),
        migrations.AddField(
            model_name='favorite',
            name='users',
            field=models.ManyToManyField(related_name='users', to=settings.AUTH_USER_MODEL),
        ),
    ]
