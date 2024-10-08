# Generated by Django 4.1.6 on 2023-05-03 00:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('loja', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Roupas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=40)),
                ('tamanho', models.CharField(max_length=4)),
                ('tipoRoupa', models.CharField(max_length=40)),
                ('estado', models.CharField(max_length=30)),
                ('descricao', models.CharField(max_length=400)),
                ('preco', models.IntegerField(default=0)),
                ('data', models.DateTimeField(verbose_name='data')),
                ('foto', models.ImageField(upload_to='')),
                ('idCliente', models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('marca', models.CharField(max_length=30)),
                ('foto', models.ImageField(upload_to='')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='clothingitem',
            name='seller',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='item',
        ),
        migrations.RemoveField(
            model_name='favorite',
            name='user',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='buyer',
        ),
        migrations.RemoveField(
            model_name='purchase',
            name='item',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
        migrations.DeleteModel(
            name='ClothingItem',
        ),
        migrations.DeleteModel(
            name='Favorite',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
        migrations.DeleteModel(
            name='Purchase',
        ),
        migrations.AddField(
            model_name='checkout',
            name='roupas',
            field=models.ManyToManyField(related_name='roupas', to='loja.roupas'),
        ),
        migrations.AddField(
            model_name='checkout',
            name='usuario',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='loja.usuario'),
        ),
    ]
