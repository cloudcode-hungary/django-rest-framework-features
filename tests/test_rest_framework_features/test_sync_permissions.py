import pytest
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework_features import models, apps

pytestmark = pytest.mark.django_db


def test_sync_permissions():
    content_type = ContentType.objects.get_for_model(models.Feature)
    permission_app = Permission.objects.create(name='app', codename='app', content_type=content_type)
    permission_test = Permission.objects.create(name='test', codename='app_test', content_type=content_type)
    permission_update_test = Permission.objects.create(name='updateTest', codename='app_test_updateTest', content_type=content_type)
    permission_get_test_under_app = Permission.objects.create(name='getTest', codename='app_getTest', content_type=content_type)

    apps.sync_permissions()

    assert not Permission.objects.filter(id=permission_update_test.id).exists()
    assert Permission.objects.get(name='app', codename='app').id == permission_app.id
    assert Permission.objects.get(name='test', codename='app_test').id == permission_test.id
    assert Permission.objects.get(name='listTests', codename='app_test_read_listTests')
    assert Permission.objects.get(name='getTest', codename='app_test_read_getTest')
    assert Permission.objects.get(name='deleteTest', codename='app_test_write_deleteTest')
