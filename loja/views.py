from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.utils import timezone
from django.contrib.auth.decorators import login_required

import loja.models
from loja.models import Usuario, Roupas, Checkout



def index(request):

    listaRoupa = Roupas.objects.all()

    if request.user.is_authenticated:

        usuario = get_object_or_404(Usuario, user=request.user.id)

        if Checkout.objects.filter(usuario=usuario).exists():

            carrinho = get_object_or_404(Checkout, usuario=usuario)
            listaCompras = carrinho.roupas.all()

            return render(request,'index.html',{'listaRoupa': listaRoupa, 'listaCompras':listaCompras})

        else:

            render(request, 'index.html', {'listaRoupa':listaRoupa})

    else:

        render(request, 'index.html',{'listaRoupa':listaRoupa} )



def loginSite(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))
        else:
            return render(request, 'loginfalhou.html')
    return render(request, 'logincerto.html')



def registarSite(request):
    if request.method == "POST":
        nome = request.POST['username']
        email = request.POST['mail']
        password = request.POST['pass']
        marca = request.POST['marca']

        if request.FILES['img']:
            foto = request.FILES['img']
            ponto = foto.name.rfind('.')
            extension = foto.name[ponto:]
            nomefotografia = nome + extension
            fs = FileSystemStorage()
            if fs.exists(nomefotografia):
                print("Já existe")
                fs.delete(nomefotografia)
            fs.save(nomefotografia, foto)
        u = User.objects.create_user(nome, email, password)
        utilizador = Usuario(user=u, marca=marca, imagem=nomefotografia)
        utilizador.save()
        return render(request, 'registocerto.html')
    return render(request, 'registo.html')

def logoutSite(request):
    logout(request)
    return render(request, 'logout.html')


def especificacoesRoupa(request, roupa_id):

    roupa = get_object_or_404(Roupas, pk=roupa_id)
    usuario = None

    if request.user.is_authenticated:

        usuario = get_object_or_404(Usuario, pk=request.user.id)


    emailUsuario = get_object_or_404(Usuario, pk=roupa.idCliente)
    email = usuario.user.email

    return render(request, 'especificacoes.html', {'roupa': roupa, 'usuario': usuario, 'email': email})


@login_required(login_url='loginrequired')
def criarAnuncio(request):
    if request.method == "POST":
        marca = request.POST['marca']
        tamanho = request.POST['tamanho']
        tipoRoupa = request.POST['tipoRoupa']
        estado = request.POST['estado']
        descricao = request.POST['descricao']
        preco = request.POST['preco']
        data = timezone.now()
        usuari = request.user
        usuario = get_object_or_404(Usuario, pk=usuari.id)
        if request.FILES['img']:
            foto = request.FILES['img']
            ponto = foto.name.rfind('.')
            extension = foto.name[ponto:]
            nomefotografia = marca + tipoRoupa + request.user.username + extension
            fs = FileSystemStorage()
            if fs.exists(nomefotografia):
                fs.delete(nomefotografia)
            fs.save(nomefotografia, foto)

        sp = loja.models.Roupas(marca=marca,
                                    tamanho=tamanho,tipoRoupa=tipoRoupa,estado=estado, descricao=descricao,
                                    preco=preco,data=data, imagem=nomefotografia, idCliente=usuario.id)

        sp.save()
        return HttpResponseRedirect(reverse('index'))
    return render(request, 'adicionaranuncio.html')


@login_required(login_url='loginrequired')
def apagaranuncio(request, roupa_id):
    sp = Roupas.objects.get(pk=roupa_id)
    sp.delete()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='loginrequired')
def perfil(request):
    usuari = request.user
    usuario = get_object_or_404(Usuario, pk=usuari.id)
    return render(request, 'perfil.html', {'usuario': usuario})


@login_required(login_url='loginrequired')
def apagarperfil(request):
    usuario = get_object_or_404(Usuario, pk=request.user.id)
    if Checkout.objects.filter(usuario=usuario).exists():
        cart = get_object_or_404(Checkout, usario=usuario)
        cart.delete()
    for i in Roupas.objects.all():
        if i.cliente_id == usuario.id:
            i.delete()
    logout(request)

    u = User.objects.get(pk=usuario.id)
    u.delete()
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='loginrequired')
def addcarrinho(request, roupa_id):
    sp = Roupas.objects.get(pk=roupa_id)
    usuario = get_object_or_404(Usuario, user=request.user.id)
    carrinho = None
    if Checkout.objects.filter(usuario=usuario).exists():
        carrinho = Checkout.objects.get(idCliente=usuario.id)

    else:
        carrinho = Checkout(usuario=usuario)
        carrinho.save()

    carrinho.roupas.add(sp)
    return HttpResponseRedirect(reverse('index'))


def apagardocarrinho(request, roupa_id):
    usuario = get_object_or_404(Usuario, user=request.user.id)
    sp = Roupas.objects.get(pk=roupa_id)
    if Checkout.objects.filter(usuario=usuario).exists():
        cart = get_object_or_404(Checkout, usuario=usuario)
        if Roupas.objects.filter(pk=sp.id):
            print("olaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
            cart.roupas.remove(sp)
    return HttpResponseRedirect(reverse('index'))


@login_required(login_url='loginrequired')
def checkout(request):
    usuario = get_object_or_404(Usuario, user=request.user.id)
    carrinho = get_object_or_404(Checkout, usuario=usuario)
    listaCompras = carrinho.roupas.all()
    return render(request, 'checkout.html', {'listaCompras': listaCompras})


@login_required(login_url='loginrequired')
def compra(request, roupas_id):
    usuario = get_object_or_404(Usuario, user=request.user.id)
    if Checkout.objects.filter(usuario=usuario).exists():
        cart = get_object_or_404(Checkout, usuario=usuario)
        listaCompras = cart.roupas.all()
        for i in listaCompras:
            i.delete()
        return render(request, 'compra.html',)
    sp = Roupas.objects.get(pk=roupas_id)
    sp.delete()
    return render(request, 'compra.html',)


def indexfiltered(request):
    if request.method == 'POST':
        marca_filtrada = Roupas.objects.filter(marca__icontains=request.POST['pesquisa'])
    return render(request, 'pesquisa.html', {'marca_filtrada': marca_filtrada })


def indexsortedup(request):
    listaRoupa = Roupas.objects.order_by('preco')
    return render(request, 'index.html', {'listaRoupa': listaRoupa})


def indexsorteddown(request):
    listaRoupa = Roupas.objects.order_by('preco').reverse()
    return render(request, 'index.html', {'listaRoupa': listaRoupa})


@login_required(login_url='loginrequired')
def comprarmultiplos(request):
    usuario = get_object_or_404(Usuario, user=request.user.id)
    if Checkout.objects.filter(usuario=usuario).exists():
        cart = get_object_or_404(Checkout, usuario=usuario)
        listaCompras = cart.roupas.all()
        for i in listaCompras:
            i.delete()
        return render(request, 'compra.html', )


@login_required(login_url='loginrequired')
def alterarpass(request):
    password = request.POST['pass']
    u = User.objects.get(username=request.user.username)
    u.set_password(password)
    u.save()
    return render(request, 'passscerta.html')


def loginrequired(request):
    return render(request, 'loginrequired.html')

















