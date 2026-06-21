from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),

    # URLS Motorista
    path('motoristas/', views.lista_motoristas, name='lista_motoristas'),
    path('motoristas/novo/', views.salvar_motorista, name='criar_motorista'),
    path('motoristas/editar/<int:pk>/', views.salvar_motorista, name='editar_motorista'),
    path('motoristas/deletar/<int:pk>/', views.deletar_motorista, name='deletar_motorista'),

    # URLS Automóvel
    path('automoveis/', views.lista_automoveis, name='lista_automoveis'),
    path('automoveis/novo/', views.salvar_automovel, name='criar_automovel'),
    path('automoveis/editar/<int:pk>/', views.salvar_automovel, name='editar_automovel'),
    path('automoveis/deletar/<int:pk>/', views.deletar_automovel, name='deletar_automovel'),

    # URLS Conserto
    path('consertos/', views.lista_consertos, name='lista_consertos'),
    path('consertos/novo/', views.salvar_conserto, name='criar_conserto'),
    path('consertos/editar/<int:pk>/', views.salvar_conserto, name='editar_conserto'),
    path('consertos/deletar/<int:pk>/', views.deletar_conserto, name='deletar_conserto'),
]