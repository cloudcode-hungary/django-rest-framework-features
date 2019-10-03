import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework_features import models, apps, urls, permissions
from ..models import User

pytestmark = pytest.mark.django_db


def test_feature_permissions_no_permission(user_factory, api_client):
    apps.sync_permissions()
    api_client.force_authenticate(user=user_factory())

    response = api_client.delete(urls.reverse('deleteTest', id=1))
    assert response.status_code == 403

    response = api_client.get(urls.reverse('listTests'))
    assert response.status_code == 403

    response = api_client.get(urls.reverse('getTest', id=1))
    assert response.status_code == 403


def test_feature_permissions_read_permission_only(user_factory, api_client):
    apps.sync_permissions()
    user = user_factory()
    content_type = ContentType.objects.get_for_model(models.Feature)
    user.user_permissions.add(Permission.objects.get(codename='app_test_read', content_type=content_type))
    api_client.force_authenticate(user=User.objects.get())

    response = api_client.delete(urls.reverse('deleteTest', id=1))
    assert response.status_code == 403

    response = api_client.get(urls.reverse('listTests'))
    assert response.status_code == 200

    response = api_client.get(urls.reverse('getTest', id=1))
    assert response.status_code == 200


def test_feature_permissions_all_permission(user_factory, api_client):
    apps.sync_permissions()
    user = user_factory()
    content_type = ContentType.objects.get_for_model(models.Feature)

    user.user_permissions.add(Permission.objects.get(codename='app', content_type=content_type))
    api_client.force_authenticate(user=User.objects.get())

    response = api_client.delete(urls.reverse('deleteTest', id=1))
    assert response.status_code == 200

    response = api_client.get(urls.reverse('listTests'))
    assert response.status_code == 200

    response = api_client.get(urls.reverse('getTest', id=1))
    assert response.status_code == 200


def test_get_codenames_from_description():
    assert permissions.get_codenames_from_description([
        'app', 'test', 'read', 'getTest',
    ]) == ['app', 'app_test', 'app_test_read', 'app_test_read_getTest']
