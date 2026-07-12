from django.db import models

# 1° Ícone / Tabela: Dados do Motorista
class Motorista(models.Model):
    # O Django cria automaticamente uma Chave Primária (id) para cada modelo
    nome = models.CharField(max_length=100, verbose_name="Nome Completo")
    cpf = models.CharField(max_length=14, unique=True, verbose_name="CPF")
    telefone = models.CharField(max_length=20, verbose_name="Telefone")
    endereco = models.TextField(verbose_name="Endereço")
    email = models.EmailField(unique=True, verbose_name="E-mail")

    def __str__(self):
        return self.nome


# 2° Ícone / Tabela: Dados do Automóvel
class Automovel(models.Model):
    marca = models.CharField(max_length=50, verbose_name="Marca")
    modelo = models.CharField(max_length=50, verbose_name="Modelo")
    ano = models.IntegerField(verbose_name="Ano")

    # Relacionamento: O automóvel pertence a um motorista (Chave Estrangeira)
    motorista = models.ForeignKey(Motorista, on_delete=models.CASCADE, related_name="automoveis", verbose_name="Proprietário/Motorista")

    def __str__(self):
        return f"{self.marca} {self.modelo} ({self.ano})"


# 3° Ícone / Tabela: Dados do Conserto
class Conserto(models.Model):
    problema_carro = models.TextField(verbose_name="Problema Relatado")
    pecas_a_trocar = models.TextField(verbose_name="Peças a serem trocadas", blank=True, null=True)
    data_entrada = models.DateTimeField(verbose_name="Data de Entrada")
    data_saida = models.DateTimeField(blank=True, null=True, verbose_name="Data de Saída")
    mecanico_responsavel = models.CharField(max_length=100, verbose_name="Mecânico Responsável")

    # Valores monetários
    valor_pecas = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor das Peças")
    valor_servico = models.DecimalField(max_digits=10, decimal_places=2, default=0.00, verbose_name="Valor do Serviço")

    # Relacionamento: O conserto é associado a um automóvel específico
    automovel = models.ForeignKey(Automovel, on_delete=models.CASCADE, related_name="consertos", verbose_name="Automóvel")

    # Propriedade calculada para o Valor Total
    @property
    def valor_total(self):
        return self.valor_pecas + self.valor_servico

    def __str__(self):
        return f"Conserto OS #{self.id} - {self.automovel.modelo}"