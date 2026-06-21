from django import forms
from .models import Motorista, Automovel, Conserto

class MotoristaForm(forms.ModelForm):
    class Meta:
        model = Motorista
        fields = '__all__'
        widgets = {
            fields: forms.TextInput(attrs={'class': 'form-control'}) for fields in ['nome', 'cpf', 'telefone', 'email']
        }
    # Campo de endereço como área de texto customizada
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['endereco'].widget = forms.Textarea(attrs={'class': 'form-control', 'rows': 3})

class AutomovelForm(forms.ModelForm):
    class Meta:
        model = Automovel
        fields = '__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class ConsertoForm(forms.ModelForm):
    class Meta:
        model = Conserto
        fields = '__all__'
        widgets = {
            'data_entrada': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'data_saida': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name not in ['data_entrada', 'data_saida']:
                field.widget.attrs.update({'class': 'form-control'})