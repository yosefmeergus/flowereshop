# Generated by Django 4.0.5 on 2022-10-16 14:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_alter_flower_cost'),
        ('accounts', '0003_alter_cartitem_cart'),
    ]

    operations = [
        migrations.CreateModel(
            name='Favorites',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='FavoritesItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('favorites', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_items', to='accounts.favorites')),
                ('flower', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='favorites_item', to='products.flower')),
            ],
        ),
    ]
