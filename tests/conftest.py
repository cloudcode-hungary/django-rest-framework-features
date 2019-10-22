import os

import factory
import pytest
from factory.django import DjangoModelFactory
from pytest_django.lazy_django import skip_if_no_django
from pytest_factoryboy import register


def pytest_configure():
    from django.conf import settings

    if 'TRAVIS' in os.environ:
        databases = {
            'default': {
                'ENGINE': 'django.db.backends.postgresql_psycopg2',
                'NAME': 'travisci',
                'USER': 'postgres',
                'PASSWORD': '',
                'HOST': 'localhost',
                'PORT': '',
            }
        }
    else:
        databases = {'default': {'ENGINE': 'django.db.backends.sqlite3',
                           'NAME': ':memory:'}}
    settings.configure(
        DEBUG_PROPAGATE_EXCEPTIONS=True,
        DATABASES=databases,
        SITE_ID=1,
        SECRET_KEY='not very secret in tests',
        USE_I18N=True,
        USE_L10N=True,
        STATIC_URL='/static/',
        ROOT_URLCONF='tests.urls',
        TEMPLATE_LOADERS=(
            'django.template.loaders.filesystem.Loader',
            'django.template.loaders.app_directories.Loader',
        ),
        TEMPLATES=[
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
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
        ],
        MIDDLEWARE_CLASSES=(
            'django.middleware.common.CommonMiddleware',
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.middleware.csrf.CsrfViewMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
        ),
        INSTALLED_APPS=(
            'django.contrib.auth',
            'django.contrib.contenttypes',
            'django.contrib.sessions',
            'django.contrib.sites',
            'django.contrib.messages',
            'django.contrib.staticfiles',

            'rest_framework',
            'rest_framework.authtoken',
            'rest_framework_features',
            'tests',
        ),
        PASSWORD_HASHERS=(
            'django.contrib.auth.hashers.SHA1PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2PasswordHasher',
            'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
            'django.contrib.auth.hashers.BCryptPasswordHasher',
            'django.contrib.auth.hashers.MD5PasswordHasher',
            'django.contrib.auth.hashers.CryptPasswordHasher',
        ),
        REST_FRAMEWORK_FEATURES={
            'ENABLE_FEATURES': False,
            'SET_HTTP_METHOD_NAMES': True,
            'SET_SCHEMA_OVERRIDE': True,
        },
        REST_FRAMEWORK={
            'DEFAULT_PERMISSION_CLASSES': (
                'rest_framework_features.permissions.CanAccessFeature',
            ),
            'DEFAULT_AUTHENTICATION_CLASSES': (
                'rest_framework.authentication.SessionAuthentication',
            ),
        }
    )

    try:
        import oauth_provider  # NOQA
        import oauth2  # NOQA
    except ImportError:
        pass
    else:
        settings.INSTALLED_APPS += (
            'oauth_provider',
        )

    try:
        import provider  # NOQA
    except ImportError:
        pass
    else:
        settings.INSTALLED_APPS += (
            'provider',
            'provider.oauth2',
        )

    # guardian is optional
    try:
        import guardian  # NOQA
    except ImportError:
        pass
    else:
        settings.ANONYMOUS_USER_ID = -1
        settings.AUTHENTICATION_BACKENDS = (
            'django.contrib.auth.backends.ModelBackend',
            'guardian.backends.ObjectPermissionBackend',
        )
        settings.INSTALLED_APPS += (
            'guardian',
        )

    try:
        import django
        django.setup()
    except AttributeError:
        pass

    from rest_framework_features import models
    from .models import User

    @register
    class UserFactory(DjangoModelFactory):
        class Meta:
            model = User

        email = factory.Sequence(lambda n: f'user_{n}@x.com')

    @register
    class AdminFactory(DjangoModelFactory):
        class Meta:
            model = User

        is_superuser = True
        email = factory.Sequence(lambda n: f'admin_{n}@x.com')

    @register
    class FeatureFactory(DjangoModelFactory):
        class Meta:
            model = models.Feature

        name = factory.Sequence(lambda n: f'feature {n}')


@pytest.fixture()
def api_client():
    """A Django test api_client instance."""
    skip_if_no_django()

    from rest_framework.test import APIClient

    return APIClient()


@pytest.fixture()
def feature_api_client(admin_factory):
    """A Django test feature_api_client instance."""
    skip_if_no_django()

    from rest_framework_features.test import FeatureAPIClient

    client = FeatureAPIClient()
    client.force_authenticate(admin_factory())
    return client
