from turtle import mode
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Roupas(models.Model):

    marca = models.CharField(max_length=40)
    tamanho = models.CharField(max_length=4)
    tipoRoupa = models.CharField(max_length=40)
    estado = models.CharField(max_length=30)
    descricao = models.CharField(max_length=400)
    preco = models.IntegerField(default=0)
    data = models.DateTimeField('data')
    foto = models.ImageField(null=False, blank=False)
    idCliente = models.IntegerField(default=0)

    def __str__(self):
        return self.marca + " " + str(self.tipoRoupa) + " " + self.tamanho + "cliente" + str(self.idCliente)


    def delete(self, *args, **kwargs):
        self.imagem.delete()
        super().delete(*args, **kwargs)




class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    marca = models.CharField(max_length=30)
    foto = models.ImageField(null=False, blank=False)

    def __str__(self):
        return self.user.username + str(self.id)

    def delete(self, *args, **kwargs):
        self.foto.delete()
        super().delete(*args, **kwargs)




class Checkout(models.Model):
    roupas = models.ManyToManyField(Roupas, related_name='roupas')
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE)
