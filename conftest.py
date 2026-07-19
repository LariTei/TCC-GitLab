import pytest
from django.contrib.auth.models import User

@pytest.fixture(scope="class", autouse=True)
def setup_banco_persistente(django_db_setup, django_db_blocker):
    """
    Esta fixture roda uma única vez por classe de teste.
    Ela permite popular dados iniciais e mantém o banco aberto e
    persistente para modificações (insert, update, delete) entre os testes.
    """
    with django_db_blocker.unblock():
        # Opcional: Você pode criar dados estáticos iniciais aqui se quiser
        # User.objects.create_user(username="admin", password="password123")

        yield  # Deixa os testes rodarem mantendo o estado do banco ativo

        # Opcional: Limpeza pesada após TODOS os testes da classe finalizarem