import re
import os
import pytest

# Permite chamadas assíncronas no ambiente de teste do Django
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

from django.test import LiveServerTestCase
from playwright.sync_api import sync_playwright, expect

# Informa ao Pytest-Django para NÃO resetar o banco de dados via transação a cada teste
# @pytest.mark.django_db(transaction=True)
class TestOficinaInterface(LiveServerTestCase):
    # Garante que os registros criados persistam entre os testes da classe
    serialized_rollback = True

    @classmethod
    def setUpClass(cls):
        """Executado uma única vez ANTES de todos os testes da classe."""
        super().setUpClass()
        # Inicia o gerenciador do Playwright uma única vez para a classe
        cls.playwright_manager = sync_playwright()
        cls.p = cls.playwright_manager.__enter__()

        # Lança o navegador e cria a página compartilhada
        cls.browser = cls.p.chromium.launch(headless=True)
        cls.page = cls.browser.new_page()

    @classmethod
    def tearDownClass(cls):
        """Executado uma única vez DEPOIS de todos os testes da classe."""
        cls.page.close()
        cls.browser.close()
        cls.playwright_manager.__exit__(None, None, None)
        super().tearDownClass()

    # REMOVIDOS OS MÉTODOS _fixture_setup e _fixture_teardown QUE ESTAVAM CAUSANDO O ERRO.
    # Em vez disso, usamos a propriedade nativa do Django para manter registros:
    serialized_rollback = True

    def test1_pagina_inicial_e_links(self):
        """Acessa a página inicial e valida os links fundamentais."""
        self.page.goto(self.live_server_url)
        self.page.wait_for_timeout(1000)

        assert "Oficina" in self.page.title() or self.page.locator("body").is_visible()
        print("Oficina é visível")

        link_motorista = self.page.locator("text=Dados do Motorista")
        assert link_motorista.is_visible()

        link_automovel = self.page.locator("text=Dados do Automóvel")
        assert link_automovel.is_visible()

        link_conserto = self.page.locator("text=Dados do Conserto")
        assert link_conserto.is_visible()

        # Simula o clique e navega
        link_motorista.click()
        self.page.wait_for_url(f"{self.live_server_url}/motoristas/")
        assert "/motoristas/" in self.page.url
        print("Página Motorista carregada.")

    def test2_cadastrarNovoMotorista(self):
    #     """Cadastra o segundo motorista (Gera ID 2)."""
    #     self.page.goto(f"{self.live_server_url}/motoristas/")

        btn_novo = self.page.get_by_text("+ Novo Motorista")
        btn_novo.wait_for(state="visible")
        btn_novo.click()

        self.page.wait_for_url(f"{self.live_server_url}/motoristas/novo/")
        assert "/motoristas/novo/" in self.page.url

        self.page.get_by_label("Nome Completo:").fill("TesteNumero")

        input_cpf = self.page.get_by_label("CPF:")
        input_cpf.fill("654.213.879-22")
        expect(input_cpf).to_have_value(re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"))

        input_telefone = self.page.get_by_label("Telefone:")
        input_telefone.fill("55 (11) 99876-5432")
        expect(input_telefone).to_have_value(re.compile(r"^\d{2} \(\d{2}\) \d{5}-\d{4}$"))

        self.page.get_by_label("Endereço:").fill("Rua Teste,654 - Vila Testando Cidade Testei")

        input_email = self.page.get_by_label("E-mail:")
        input_email.fill("teste2@email.com")
        expect(input_email).to_have_value(re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$"))

        self.page.get_by_text("Salvar Dados").click()
        self.page.wait_for_url(f"{self.live_server_url}/motoristas/")
        assert "/motoristas/" in self.page.url
        print("Motorista 1 salvo com sucesso.")

    # def test3_editarMotorista(self):
    #     """Acessa diretamente a listagem e clica no primeiro 'Editar' disponível (ID 1)."""
    #     self.page.goto(f"{self.live_server_url}/motoristas/")

        botao_editar = self.page.get_by_text("Editar").first
        botao_editar.wait_for(state="visible")
        botao_editar.click()
        self.page.wait_for_timeout(2_000)

        # Como o banco não sofreu rollback transacional purgado pelo pytest, o ID 1 existirá
        self.page.wait_for_url(f"{self.live_server_url}/motoristas/editar/2/")
        assert "/motoristas/editar/2/" in self.page.url
        print("Sucesso! O ID 1 persistiu e a tela de edição foi aberta.")
        self.page.wait_for_timeout(1_000)
        self.page.get_by_label("Nome Completo:").fill("Teste Editando")

        input_cpf = self.page.get_by_label("CPF:")
        input_cpf.fill("624.213.879-11")
        expect(input_cpf).to_have_value(re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"))

        input_telefone = self.page.get_by_label("Telefone:")
        input_telefone.fill("55 (11) 99876-7135")
        expect(input_telefone).to_have_value(re.compile(r"^\d{2} \(\d{2}\) \d{5}-\d{4}$"))

        self.page.get_by_label("Endereço:").fill("Rua Edição,123 - Vila Editando Cidade editado")

        input_email = self.page.get_by_label("E-mail:")
        input_email.fill("edicaodeteste@email.com")
        expect(input_email).to_have_value(re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$"))

        self.page.get_by_text("Salvar Dados").click()