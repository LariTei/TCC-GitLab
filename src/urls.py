from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

# Importa o módulo inteiro e também as ViewSets específicas para a API
from . import api_views
from .api_views import MotoristaViewSet, AutomovelViewSet, ConsertoViewSet

# Criar e registrar o roteador da API REST
router = DefaultRouter()
router.register(r'motoristas', MotoristaViewSet, basename='motorista')
router.register(r'automoveis', AutomovelViewSet, basename='automovel')
router.register(r'consertos', ConsertoViewSet, basename='conserto')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', api_views.index, name='index'),
    path('api/', include(router.urls)),

    # URLS Motorista (Web / HTML)
    path('motoristas/', api_views.lista_motoristas, name='lista_motoristas'),
    path('motoristas/novo/', api_views.salvar_motorista, name='criar_motorista'),
    path('motoristas/editar/<int:pk>/', api_views.salvar_motorista, name='editar_motorista'),
    path('motoristas/deletar/<int:pk>/', api_views.deletar_motorista, name='deletar_motorista'),

    # URLS Automóvel (Web / HTML)
    path('automoveis/', api_views.lista_automoveis, name='lista_automoveis'),
    path('automoveis/novo/', api_views.salvar_automovel, name='criar_automovel'),
    path('automoveis/editar/<int:pk>/', api_views.salvar_automovel, name='editar_automovel'),
    path('automoveis/deletar/<int:pk>/', api_views.deletar_automovel, name='deletar_automovel'),

    # URLS Conserto (Web / HTML)
    path('consertos/', api_views.lista_consertos, name='lista_consertos'),
    path('consertos/novo/', api_views.salvar_conserto, name='criar_conserto'),
    path('consertos/editar/<int:pk>/', api_views.salvar_conserto, name='editar_conserto'),
    path('consertos/deletar/<int:pk>/', api_views.deletar_conserto, name='deletar_conserto'),
]