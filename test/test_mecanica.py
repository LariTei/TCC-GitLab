import re

import pytest
import os
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
from django.test import LiveServerTestCase
from playwright.sync_api import sync_playwright, Page, expect
from django.contrib.auth.models import User

class TestOficinaInterface(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        """Executado uma única vez ANTES de todos os testes da classe."""
        super().setUpClass()
        # Inicia o gerenciador do Playwright e guarda na classe para podermos fechar depois
        cls.playwright_manager = sync_playwright()
        cls.p = cls.playwright_manager.__enter__()

        # Lança o navegador e cria a página que será compartilhada por todos os testes
        cls.browser = cls.p.chromium.launch(headless=False)
        cls.page = cls.browser.new_page()

    @classmethod
    def tearDownClass(cls):
        """Executado uma única vez DEPOIS de todos os testes da classe terem finalizado."""
        cls.browser.close()
        cls.playwright_manager.__exit__(None, None, None)
        super().tearDownClass()

    def test1_pagina_inicial_e_links(self):
        """
        Este teste inicia o servidor Django automaticamente em segundo plano,
        abre o navegador via Playwright, acessa a página inicial e valida os ícones.
        """
        self.page.goto(self.live_server_url)
        self.page.wait_for_timeout(1_000)

        # 3. Validações na Página Inicial (Exemplo baseado na Oficina Mecânica)
        # Verifica se o título ou algum elemento principal está na tela
        assert "Oficina" in self.page.title() or self.page.locator("body").is_visible()
        print("Oficina é visivel")
        self.page.wait_for_timeout(2_000)

        # Exemplo: Validando se os links ou botões correspondentes aos ícones existem
        # Ícone 1: Dados do Motorista
        link_motorista = self.page.locator("text=Dados do Motorista")
        assert link_motorista.is_visible()
        print("Motorista é visivel")
        self.page.wait_for_timeout(2_000)

        # Ícone 2: Dados do Automóvel
        link_automovel = self.page.locator("text=Dados do Automóvel")
        assert link_automovel.is_visible()
        print("Automovel é visivel")
        self.page.wait_for_timeout(2_000)

        # Ícone 3: Dados do Conserto
        link_conserto = self.page.locator("text=Dados do Conserto")
        assert link_conserto.is_visible()
        print("Dados do Concerto é visivel")
        self.page.wait_for_timeout(2_000)

        # 4. Simula o clique no ícone de Motoristas para testar a navegação
        link_motorista.click()

        # Espera a nova URL carregar e valida se mudou de página com sucesso
        self.page.wait_for_url(f"{self.live_server_url}/motoristas/")
        assert "/motoristas/" in self.page.url
        print("Pagina Motorista")
        self.page.wait_for_timeout(2_000)

    def test2_cadastro_motorista(self):
        self.page.get_by_text("+ Novo Motorista").is_visible()
        self.page.get_by_text("+ Novo Motorista").click()
        self.page.wait_for_timeout(2_000)
        self.page.wait_for_url(f"{self.live_server_url}/motoristas/novo/")
        assert "/motoristas/novo/" in self.page.url

        #Preenchendo o campo Nome Completo
        self.page.get_by_label("Nome Completo:").is_visible()
        self.page.get_by_label("Nome Completo:").fill("TesteNumero1")
        print("Preenchendo campo nome")
        self.page.wait_for_timeout(2_000)
        #Preenchendo o campo CPF
        input_cpf = self.page.get_by_label("CPF:")
        input_cpf.is_visible()
        input_cpf.fill("123.456.789-10")
        self.page.wait_for_timeout(2_000)
        #validando o campo CPF
        expect(input_cpf).to_have_value(re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"))
        #preenchendo o campo Telefone
        input_telefone = self.page.get_by_label("Telefone:")
        input_telefone.is_visible()
        input_telefone.fill("55 (11) 91234-5678")
        self.page.wait_for_timeout(2_000)
        #validando o campo Telefone
        expect(input_telefone).to_have_value(re.compile(r"^\d{2} \(\d{2}\) \d{5}-\d{4}$" ))
        #Preenchendo o campo Endereço
        self.page.get_by_label("Endereço:").is_visible()
        self.page.get_by_label("Endereço:").fill("Rua Teste,123 - Vila Testando Cidade Testei")
        self.page.wait_for_timeout(2_000)
        #Preenchendo o campo email
        input_email = self.page.get_by_label("E-mail:")
        input_email.is_visible()
        input_email.fill("teste@email.com")
        self.page.wait_for_timeout(2_000)
        #Validando o campo Email
        regex_email = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$")
        expect(input_email).to_have_value(regex_email)
        #Salvando motorista
        self.page.get_by_text("Salvar Dados").is_visible()
        self.page.get_by_text("Salvar Dados").click()
        self.page.wait_for_timeout(2_000)

    def test3_cadastrarNovoMotorista(self):
        self.page.get_by_text("+ Novo Motorista").is_visible()
        self.page.get_by_text("+ Novo Motorista").click()
        self.page.wait_for_timeout(2_000)
        self.page.wait_for_url(f"{self.live_server_url}/motoristas/novo/")
        assert "/motoristas/novo/" in self.page.url

        #Preenchendo o campo Nome Completo
        self.page.get_by_label("Nome Completo:").is_visible()
        self.page.get_by_label("Nome Completo:").fill("TesteNumero2")
        print("Preenchendo campo nome")
        self.page.wait_for_timeout(2_000)
        #Preenchendo o campo CPF
        input_cpf = self.page.get_by_label("CPF:")
        input_cpf.is_visible()
        input_cpf.fill("654.213.879-22")
        self.page.wait_for_timeout(2_000)
        #validando o campo CPF
        expect(input_cpf).to_have_value(re.compile(r"^\d{3}\.\d{3}\.\d{3}-\d{2}$"))
        #preenchendo o campo Telefone
        input_telefone = self.page.get_by_label("Telefone:")
        input_telefone.is_visible()
        input_telefone.fill("55 (11) 99876-5432")
        self.page.wait_for_timeout(2_000)
        #validando o campo Telefone
        expect(input_telefone).to_have_value(re.compile(r"^\d{2} \(\d{2}\) \d{5}-\d{4}$" ))
        #Preenchendo o campo Endereço
        self.page.get_by_label("Endereço:").is_visible()
        self.page.get_by_label("Endereço:").fill("Rua Teste,654 - Vila Testando Cidade Testei")
        self.page.wait_for_timeout(2_000)
        #Preenchendo o campo email
        input_email = self.page.get_by_label("E-mail:")
        input_email.is_visible()
        input_email.fill("teste2@email.com")
        self.page.wait_for_timeout(2_000)
        #Validando o campo Email
        regex_email = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.com$")
        expect(input_email).to_have_value(regex_email)
        #Salvando motorista
        self.page.get_by_text("Salvar Dados").is_visible()
        self.page.get_by_text("Salvar Dados").click()
        self.page.wait_for_timeout(2_000)
        assert "/motoristas/" in self.page.url

    def test4_editarMotorista(self):
        self.page.get_by_text("Editar").is_visible()
        self.page.get_by_text("Editar").first.click()
        self.page.wait_for_url(f"{self.live_server_url}/motoristas/editar/1")
        assert "/motoristas/editar/1" in self.page.url
        self.page.wait_for_timeout(5_000)

    # def test5_deletarMotorista(self):



