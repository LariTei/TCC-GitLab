import pytest
from django.db import connection
from django.contrib.auth.models import User
from django.db.backends.sqlite3.base import DatabaseWrapper

# Desabilita a verificação estrita de threads do SQLite para ambientes de teste multithread
DatabaseWrapper.validate_thread_sharing = lambda self: None

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

# @pytest.fixture(autouse=True)
# def enable_db_thread_sharing():
#     # Permite que qualquer thread acesse e feche a conexão do SQLite durante os testes
#     connection.allow_thread_sharing = True
#     yield

@pytest.fixture(autouse=True)
def enable_db_thread_sharing(db):
    # Permite o compartilhamento de thread explicitamente
    connection.inc_thread_sharing()
    yield
    # Fecha a conexão após o término do teste para evitar vazamento
    connection.close()

@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        connection.inc_thread_sharing()