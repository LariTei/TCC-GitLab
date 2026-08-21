# test/test_api_integration.py
import pytest
from rest_framework.test import APIClient
from rest_framework import status
from src.models import Motorista, Automovel, Conserto

@pytest.mark.django_db
class TestAPIIntegracaoOficina:

    @pytest.fixture(autouse=True)
    def setup(self):
        """Inicializa o cliente de testes da API do DRF"""
        self.client = APIClient()

    def test1_criacao_motorista_via_api_e_persistencia_no_banco(self):
        """Testa se POST na API grava com sucesso o registro no banco de dados"""
        payload = {
            "nome": "Carlos Silva",
            "cpf": "123.456.789-00",
            "telefone": "(11) 98765-4321",
            "endereco": "Rua A, 123",
            "email": "carlos@email.com"
        }
        response = self.client.post('/api/motoristas/', payload, format='json')

        # 1. Valida Resposta HTTP da API
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["nome"] == "Carlos Silva"

        # 2. Valida persistência direta no Banco de Dados
        assert Motorista.objects.count() == 1
        motorista_db = Motorista.objects.get(cpf="123.456.789-00")
        assert motorista_db.nome == "Carlos Silva"

    def test2_integracao_relacionamento_motorista_automovel_e_conserto(self):
        # 1. Criar Motorista no banco de dados
        motorista = Motorista.objects.create(
            nome="Ana Souza",
            cpf="987.654.321-11",
            telefone="11911112222",
            endereco="Rua B",
            email="ana@email.com"
        )

        # 2. Criar Automóvel via API
        payload_auto = {
            "marca": "Toyota",
            "modelo": "Corolla",
            "ano": 2022,
            "motorista": motorista.id
        }
        res_auto = self.client.post('/api/automoveis/', payload_auto, format='json')
        assert res_auto.status_code == status.HTTP_201_CREATED
        auto_id = res_auto.data['id']

        # 3. Criar Conserto via API
        payload_conserto = {
            "automovel": auto_id,
            "problema_carro": "Troca de óleo e filtro",
            "pecas_a_trocar": "Óleo 5W30, Filtro de Óleo",
            "data_entrada": "2026-07-20",
            "data_saida": "2026-07-21",
            "mecanico_responsavel": "Roberto",
            "valor_pecas": 150.00,
            "valor_servico": 100.00
        }

        res_conserto = self.client.post('/api/consertos/', payload_conserto, format='json')

        # Se houver falha, imprime a mensagem de erro exata do DRF
        if res_conserto.status_code != status.HTTP_201_CREATED:
            print("\nDetalhes da rejeição do DRF:", res_conserto.data)

        # Asserções
        print("ERRO DE VALIDAÇÃO:", res_conserto.data)
        assert res_conserto.status_code == status.HTTP_201_CREATED
        assert float(res_conserto.data['valor_total']) == 250.00

        # Validação direta com a ORM do Banco de Dados
        conserto_db = Conserto.objects.get(id=res_conserto.data['id'])
        assert conserto_db.automovel.motorista.nome == "Ana Souza"

    def test3_atualizacao_e_exclusao_via_api(self):
        """Testa alteração (PUT) e deleção (DELETE) refletindo no banco de dados"""
        motorista = Motorista.objects.create(
            nome="Lucas Lima", cpf="111.222.333-44",
            telefone="11900000000", endereco="Rua C", email="lucas@email.com"
        )

        # Atualizar nome via PUT na API
        res_update = self.client.put(
            f'/api/motoristas/{motorista.id}/',
            {
                "nome": "Lucas Lima Alterado",
                "cpf": "111.222.333-44",
                "telefone": "11900000000",
                "endereco": "Rua C Nova",
                "email": "lucas@email.com"
            },
            format='json'
        )
        assert res_update.status_code == status.HTTP_200_OK

        # Validar alteração no Banco
        motorista.refresh_from_db()
        assert motorista.nome == "Lucas Lima Alterado"

        # Excluir via DELETE na API
        res_delete = self.client.delete(f'/api/motoristas/{motorista.id}/')
        assert res_delete.status_code == status.HTTP_204_NO_CONTENT

        # Confirmar que foi removido do Banco
        assert Motorista.objects.filter(id=motorista.id).count() == 0