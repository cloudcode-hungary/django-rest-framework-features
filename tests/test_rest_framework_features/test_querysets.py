import pytest

from rest_framework_features import models

pytestmark = pytest.mark.django_db


def test_feature_queryset_with_levels(feature_factory):
    feature_e = feature_factory(name='e')
    feature_d = feature_factory(name='d', parent=feature_e)
    feature_c = feature_factory(name='c', parent=feature_e)
    feature_b = feature_factory(name='b', parent=feature_c)
    feature_a = feature_factory(name='a', parent=feature_c)
    feature_f = feature_factory(name='f')

    queryset = models.Feature.objects.with_display_names()

    assert queryset[0].id == feature_e.id
    assert queryset[0].display_name == 'e'
    assert queryset[1].id == feature_c.id
    assert queryset[1].display_name == 'e/c'
    assert queryset[2].id == feature_a.id
    assert queryset[2].display_name == 'e/c/a'
    assert queryset[3].id == feature_b.id
    assert queryset[3].display_name == 'e/c/b'
    assert queryset[4].id == feature_d.id
    assert queryset[4].display_name == 'e/d'
    assert queryset[5].id == feature_f.id
    assert queryset[5].display_name == 'f'
    assert len(queryset) == 6
