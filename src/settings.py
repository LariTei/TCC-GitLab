import os
from pathlib import Path
import sys

# Caminho base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# 1. Definição padrão do banco de dados (OBRIGATÓRIO vir antes)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# 2. Sobrescrita específica para o ambiente de testes (Pytest)
if 'pytest' in sys.modules or 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'test_db.sqlite3',
        'OPTIONS': {
            'timeout': 30,
            'check_same_thread': False,
        },
    }
# CONFIGURAÇÕES DE SEGURANÇA (Para desenvolvimento local)
SECRET_KEY = 'django-insecure-oficina-mecanica-chave-temporaria'
DEBUG = True
ALLOWED_HOSTS = []

# APLICATIVOS REGISTRADOS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Adicione a aplicação da API REST
    'rest_framework',
    'src',  # Registra a sua pasta atual como um app do Django
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'src.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'src.wsgi.application'

# BANCO DE DADOS (Usando SQLite3 local para facilitar)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'db.sqlite3'),
        'TEST': {
            # Força o banco de testes a rodar em memória, evitando travas no Windows
            'NAME': ':memory:',
        },
    }
}

# VALIDAÇÃO DE SENHAS
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# LOCALIZAÇÃO (Configurado para o Brasil)
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# ARQUIVOS ESTÁTICOS (CSS, JS, Imagens)
STATIC_URL = 'static/'
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Se estiver executando via pytest
if 'pytest' in sys.modules:
    DATABASES['default']['OPTIONS'] = {
        'timeout': 20,
        'check_same_thread': False,  # Permite que threads paralelas usem o mesmo SQLite
    }