import pytest

pytestmark = pytest.mark.django_db


def test_feature_api_client(feature_api_client):
    response = feature_api_client('listTests')
    assert response.status_code == 200

    response = feature_api_client('getTest', kwargs={'id': 1})
    assert response.status_code == 200
