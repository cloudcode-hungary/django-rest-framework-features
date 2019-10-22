import pytest

from rest_framework_features import models, apps

pytestmark = pytest.mark.django_db


def test_sync_features(feature_factory):
    feature_app = feature_factory(name='app')
    feature_test = feature_factory(name='test', parent=feature_app)
    feature_update_test = feature_factory(name='updateTest', parent=feature_test)
    feature_get_test_under_app = feature_factory(name='getTest', parent=feature_app)     # noqa F841

    apps.sync_features()

    assert not models.Feature.objects.filter(id=feature_update_test.id).exists()
    assert models.Feature.objects.count() == 7
    assert models.Feature.objects.get(name='app', parent=None).id == feature_app.id
    assert models.Feature.objects.get(name='test', parent=feature_app).id == feature_test.id
    feature_read = models.Feature.objects.get(name='read', parent=feature_test)
    feature_write = models.Feature.objects.get(name='write', parent=feature_test)
    assert models.Feature.objects.get(name='listTests', parent=feature_read)
    assert models.Feature.objects.get(name='getTest', parent=feature_read)
    assert models.Feature.objects.get(name='deleteTest', parent=feature_write)
