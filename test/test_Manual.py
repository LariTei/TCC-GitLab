import os
import time
import threading
from django.test.testcases import LiveServerTestCase
from playwright.sync_api import sync_playwright

# Garante permissão para operações assíncronas se necessário
os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

class ManualLiveServerRunner(LiveServerTestCase):
    """
    Sobe o Live Server do Django e abre o navegador visível (headless=False)
    para execução e testes manuais na tela, preservando o estado do banco.
    """

    # Define a porta fixa opcionalmente (ex: 8081) ou deixa o Django escolher uma livre
    port = 8081

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Inicializa o Playwright em modo visível
        cls.playwright = sync_playwright().start()
        cls.browser = cls.playwright.chromium.launch(headless=False, slow_mo=500)
        cls.context = cls.browser.new_context()
        cls.page = cls.context.new_page()

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()
        super().tearDownClass()

    def test_executar_modo_manual_interativo(self):
        # URL gerada dinamicamente pelo LiveServerTestCase do Django
        url_alvo = f"{self.live_server_url}/motoristas/"

        print("\n" + "="*70)
        print(f"🚀 LIVE SERVER RODANDO EM: {self.live_server_url}")
        print(f"🌐 Acessando a página inicial: {url_alvo}")
        print("💡 O navegador foi aberto de forma visível.")
        print("👉 Você pode interagir com o site manualmente, cadastrar motoristas, etc.")
        print("⏸️  Pressione [ENTER] neste terminal quando terminar para encerrar...")
        print("="*70 + "\n")

        # Abre a página no navegador controlado pelo Playwright
        self.page.goto(url_alvo)

        # Pausa o script travando a execução até que o usuário pressione ENTER no terminal
        input()


# Se quiser executar diretamente via python nome_do_arquivo.py
if __name__ == "__main__":
    import pytest
    import sys
    # Roda o teste isolado utilizando o pytest de forma programática
    sys.exit(pytest.main(["-s", __file__]))