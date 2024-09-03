from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.loginSite, name='loginSite'),
    path('registar', views.registarSite, name='registarSite'),
    path('logout', views.logoutSite, name='logoutSite'),
    path("roupas/<int:roupas_id>", views.especificacoesRoupa, name='especificacoesRoupa'),
    path('novoanuncio', views.criarAnuncio, name='criarAnuncio'),
    path('<int:roupas_id>/apagaranuncio', views.apagaranuncio, name='apagaranuncio'),
    path('perfil', views.perfil, name='perfil'),
    path('apagarperfil', views.apagarperfil, name='apagarperfil'),
    path('<int:roupas_id>/addcarrinho', views.addcarrinho, name='addcarrinho'),
    path('<int:smartphone_id>/apagardocarrinho', views.apagardocarrinho, name='apagardocarrinho'),
    path('checkout', views.checkout, name='checkout'),
    path('<int:roupas_id>/compra', views.compra, name='compra'),
    path('indexfiltered', views.indexfiltered, name='indexfiltered'),
    path('apagaranuncio', views.apagaranuncio, name='apagaranuncio'),
    path('indexsortedup', views.indexsortedup, name='indexsortedup'),
    path('indexsorteddown', views.indexsorteddown, name='indexsorteddown'),
    path('comprarmultiplos', views.comprarmultiplos, name='comprarmultiplos'),
    path('alterarpass', views.alterarpass, name='alterarpass'),
    path('loginrequired', views.loginrequired, name='loginrequired'),
]