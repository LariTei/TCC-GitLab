# test_mecanica_pytest.py
import time
import os
import pytest
from playwright.sync_api import sync_playwright, expect

os.environ["DJANGO_ALLOW_ASYNC_UNSAFE"] = "true"

# --- fixtures para Playwright ---
@pytest.fixture(scope="session")
def playwright_manager():
    p = sync_playwright().start()
    yield p
    try:
        p.stop()
    except Exception:
        pass

@pytest.fixture(scope="session")
def browser(playwright_manager):
    browser = playwright_manager.chromium.launch(headless=False)
    yield browser
    try:
        browser.close()
    except Exception:
        pass

@pytest.fixture(scope="function")
def page(browser):
    context = browser.new_context()
    page = context.new_page()
    yield page
    try:
        page.close()
    except Exception:
        pass
    try:
        context.close()
    except Exception:
        pass

# --- testes ---
def test1_pagina_inicial_e_links(live_server, page):
    page.goto(live_server.url)
    page.wait_for_timeout(1000)
    assert "Oficina" in page.title() or page.locator("body").is_visible()
    link_motorista = page.locator("text=Dados do Motorista")
    assert link_motorista.is_visible()
    link_motorista.click()
    page.wait_for_url(f"{live_server.url}/motoristas/")
    assert "/motoristas/" in page.url

def test2_cadastrarNovoMotorista(live_server, page):
    page.goto(f"{live_server.url}/motoristas/")
    btn_novo = page.get_by_text("+ Novo Motorista")
    btn_novo.wait_for(state="visible", timeout=10_000)
    btn_novo.click()
    page.wait_for_url(f"{live_server.url}/motoristas/novo/", timeout=10_000)
    page.get_by_label("Nome Completo:").fill("TesteNumero")
    page.get_by_label("CPF:").fill("654.213.879-22")
    page.get_by_label("Telefone:").fill("55 (11) 99876-5432")
    page.get_by_label("Endereço:").fill("Rua Teste,654 - Vila Testando Cidade Testei")
    page.get_by_label("E-mail:").fill("teste2@email.com")
    page.get_by_text("Salvar Dados").click()
    page.wait_for_url(f"{live_server.url}/motoristas/", timeout=10_000)
    page.wait_for_timeout(1_000)

