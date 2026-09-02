# import pytest
# from django.test import LiveServerTestCase
# from playwright.sync_api import Page, expect, sync_playwright
# import os
# os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"
#
# class TestE2EOficinaMecanica(LiveServerTestCase):
#     """Classe de testes E2E com Playwright cobrindo o fluxo completo de cadastro,
#
#     atualização, associação de veículos e ordens de conserto.
#     """
#
#     @classmethod
#     def setUpClass(cls):
#         super().setUpClass()
#         cls.playwright = sync_playwright().start()
#         cls.browser = cls.playwright.chromium.launch(headless=True)
#
#     @classmethod
#     def tearDownClass(cls):
#         cls.browser.close()
#         cls.playwright.stop()
#         super().tearDownClass()
#
#     def setUp(self):
#         super().setUp()
#         self.page = self.browser.new_page()
#
#     def tearDown(self):
#         self.page.close()
#         super().tearDown()
#
#     @pytest.mark.django_db(transaction=True)
#     def test_fluxo_completo_e2e_oficina(self):
#         # Base URL dinamica do LiveServerTestCase
#         base_url = self.live_server_url
#
#         # -------------------------------------------------------------------
#         # 1. Cadastro do Primeiro Motorista
#         # ----------------------------------------- --------------------------
#         self.page.goto(f"{base_url}/motoristas/novo/")
#
#         self.page.fill('input[name="nome"]', "Carlos Silva")
#         self.page.fill('input[name="cpf"]', "123.456.789-00")
#         self.page.fill('input[name="telefone"]', "(11) 98765-4321")
#         self.page.fill('textarea[name="endereco"]', "Rua A, 123")
#         self.page.fill('input[name="email"]', "carlos@email.com")
#         self.page.click('button[type="submit"]')
#
#         # Valida redirecionamento ou mensagem de sucesso na tabela
#         expect(self.page.locator("body")).to_contain_text("Carlos Silva")
#
#         # -------------------------------------------------------------------
#         # 2. Cadastro do Segundo Motorista
#         # -------------------------------------------------------------------
#         self.page.goto(f"{base_url}/motoristas/novo/")
#
#         self.page.fill('input[name="nome"]', "Ana Souza")
#         self.page.fill('input[name="cpf"]', "987.654.321-11")
#         self.page.fill('input[name="telefone"]', "(11) 91111-2222")
#         self.page.fill('textarea[name="endereco"]', "Rua B, 456")
#         self.page.fill('input[name="email"]', "ana@email.com")
#         self.page.click('button[type="submit"]')
#
#         expect(self.page.locator("body")).to_contain_text("Ana Souza")
#
#         # -------------------------------------------------------------------
#         # 3. Atualização de Informação do Motorista (Carlos Silva)
#         # -------------------------------------------------------------------
#         self.page.goto(f"{base_url}/motoristas/")
#
#         # Clica no botão de editar referente ao motorista Carlos
#         self.page.click("tr:has-text('Carlos Silva') .btn-warning")
#
#         self.page.fill('input[name="nome"]', "Carlos Silva Alterado")
#         self.page.fill('textarea[name="endereco"]', "Rua Nova, 999")
#         self.page.click('button[type="submit"]')
#
#         expect(self.page.locator("body")).to_contain_text(
#             "Carlos Silva Alterado"
#         )
#
#         # -------------------------------------------------------------------
#         # 4. Cadastro de Automóvel e Vínculo com Motorista
#         # -------------------------------------------------------------------
#         self.page.goto(f"{base_url}/automoveis/novo/")
#
#         self.page.fill('input[name="marca"]', "Toyota")
#         self.page.fill('input[name="modelo"]', "Corolla")
#         self.page.fill('input[name="ano"]', "2022")
#
#         # Seleciona o motorista Carlos no dropdown/select pelo texto ou valor
#         self.page.select_option('select[name="motorista"]', label="Carlos Silva Alterado")
#         self.page.click('button[type="submit"]')
#
#         expect(self.page.locator("body")).to_contain_text("Corolla")
#
#         # -------------------------------------------------------------------
#         # 5. Cadastro do Conserto (Vinculado ao Automóvel)
#         # -------------------------------------------------------------------
#         self.page.goto(f"{base_url}/consertos/novo/")
#
#         # Seleciona o veículo cadastrado
#         self.page.select_option('select[name="automovel"]', label="Toyota Corolla (2022)")
#
#         self.page.fill(
#             'textarea[name="problema_carro"]', "Barulho ao frear"
#         )
#         self.page.fill(
#             'textarea[name="pecas_a_trocar"]', "Pastilhas de freio"
#         )
#         # Use datetime-local format required by the form widgets (YYYY-MM-DDTHH:MM)
#         self.page.fill('input[name="data_entrada"]', "2026-08-20T10:00")
#         self.page.fill('input[name="data_saida"]', "2026-08-22T15:00")
#         self.page.fill(
#             'input[name="mecanico_responsavel"]', "Roberto Mecânico"
#         )
#         self.page.fill('input[name="valor_pecas"]', "250.00")
#         self.page.fill('input[name="valor_servico"]', "150.00")
#
#         self.page.click('button[type="submit"]')
#
#         # Valida se a Ordem de Serviço foi gravada e exibida na tela
#         expect(self.page.locator("body")).to_contain_text("Barulho ao frear")
#         expect(self.page.locator("body")).to_contain_text("Roberto Mecânico")