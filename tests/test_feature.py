import pytest

from django.urls import reverse
from rest_framework_features import Feature

pytestmark = pytest.mark.django_db


def test_feature_url_resolve():
    # url_pattern = reverse('test-viewkk')
    from rest_framework_features.urls import reverse
    reverse('getTest')
