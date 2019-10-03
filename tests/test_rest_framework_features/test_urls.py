from django.urls import reverse as django_reverse

from rest_framework_features.urls import reverse


def test_url_resolve():
    assert django_reverse('test-list-view') == reverse('listTests')


def test_url_resolve_with_kwargs():
    assert django_reverse('test-retrieve-view', kwargs={'pk': 1, }) == reverse('getTest', id=1)
