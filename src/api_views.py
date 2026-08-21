from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Motorista, Automovel, Conserto
from .forms import MotoristaForm, AutomovelForm, ConsertoForm
from .serializers import MotoristaSerializer, AutomovelSerializer, ConsertoSerializer

# ==========================================
# 1. VIEWSETS (Para a API REST Framework)
# ==========================================
class MotoristaViewSet(viewsets.ModelViewSet):
    queryset = Motorista.objects.all()
    serializer_class = MotoristaSerializer

class AutomovelViewSet(viewsets.ModelViewSet):
    queryset = Automovel.objects.all()
    serializer_class = AutomovelSerializer

class ConsertoViewSet(viewsets.ModelViewSet):
    queryset = Conserto.objects.all()
    serializer_class = ConsertoSerializer


# ==========================================
# 2. VIEWS TRADICIONAIS (Para as páginas HTML)
# ==========================================

# Página Inicial (Menu com Ícones Linkáveis)
def index(request):
    return render(request, 'index.html')

# --- CRUD MOTORISTA ---
def lista_motoristas(request):
    motoristas = Motorista.objects.all()
    return render(request, 'crud/lista_motoristas.html', {'motoristas': motoristas})

def salvar_motorista(request, pk=None):
    motorista = get_object_or_404(Motorista, pk=pk) if pk else None
    form = MotoristaForm(request.POST or None, instance=motorista)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_motoristas')
    return render(request, 'crud/form_generico.html', {'form': form, 'titulo': 'Cadastrar/Editar Motorista', 'voltar': 'lista_motoristas'})

def deletar_motorista(request, pk):
    motorista = get_object_or_404(Motorista, pk=pk)
    if request.method == 'POST':
        motorista.delete()
        return redirect('lista_motoristas')
    return render(request, 'crud/confirmar_delecao.html', {'objeto': motorista, 'voltar': 'lista_motoristas'})

# --- CRUD AUTOMOVEL ---
def lista_automoveis(request):
    automoveis = Automovel.objects.all()
    return render(request, 'crud/lista_automoveis.html', {'automoveis': automoveis})

def salvar_automovel(request, pk=None):
    automovel = get_object_or_404(Automovel, pk=pk) if pk else None
    form = AutomovelForm(request.POST or None, instance=automovel)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_automoveis')
    return render(request, 'crud/form_generico.html', {'form': form, 'titulo': 'Cadastrar/Editar Automóvel', 'voltar': 'lista_automoveis'})

def deletar_automovel(request, pk):
    automovel = get_object_or_404(Automovel, pk=pk)
    if request.method == 'POST':
        automovel.delete()
        return redirect('lista_automoveis')
    return render(request, 'crud/confirmar_delecao.html', {'objeto': automovel, 'voltar': 'lista_automoveis'})

# --- CRUD CONSERTO ---
def lista_consertos(request):
    consertos = Conserto.objects.all()
    return render(request, 'crud/lista_consertos.html', {'consertos': consertos})

def salvar_conserto(request, pk=None):
    conserto = get_object_or_404(Conserto, pk=pk) if pk else None
    form = ConsertoForm(request.POST or None, instance=conserto)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('lista_consertos')
    return render(request, 'crud/form_generico.html', {'form': form, 'titulo': 'Cadastrar/Editar Ordem de Conserto', 'voltar': 'lista_consertos'})

def deletar_conserto(request, pk):
    conserto = get_object_or_404(Conserto, pk=pk)
    if request.method == 'POST':
        conserto.delete()
        return redirect('lista_consertos')
    return render(request, 'crud/confirmar_delecao.html', {'objeto': conserto, 'voltar': 'lista_consertos'})