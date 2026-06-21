from django.contrib import admin
from .models import Motorista, Automovel, Conserto

# Customização para exibição dos dados no painel


@admin.register(Motorista)
class MotoristaAdmin(admin.ModelAdmin):
    # Colunas que vão aparecer na listagem
    list_display = ('nome', 'cpf', 'telefone', 'email')
    # Barra de pesquisa por nome ou CPF
    search_fields = ('nome', 'cpf')


@admin.register(Automovel)
class AutomovelAdmin(admin.ModelAdmin):
    list_display = ('marca', 'modelo', 'ano', 'motorista')
    list_filter = ('marca', 'ano')
    search_fields = ('modelo', 'motorista__nome')


@admin.register(Conserto)
class ConsertoAdmin(admin.ModelAdmin):
    list_display = ('id', 'automovel', 'mecanico_responsavel',
                    'data_entrada', 'valor_pecas', 'valor_servico', 'get_valor_total')
    list_filter = ('mecanico_responsavel', 'data_entrada')

    # Função para exibir a propriedade calculada 'valor_total' na tabela do painel
    def get_valor_total(self, obj):
        return f"R$ {obj.valor_total}"
    get_valor_total.short_description = 'Valor Total'