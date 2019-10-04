from rest_framework_features import schema
from tests.views import TestListView, TestInstanceView


def test_feature_view_decorator():
    description, http_method_name, view_class = getattr(TestListView, schema.REGISTRY_ATTR_NAME)['get']
    assert description == ['app', 'test', 'read', 'listTests']
    assert http_method_name == 'get'
    assert view_class == TestListView

    description, http_method_name, view_class = getattr(TestInstanceView, schema.REGISTRY_ATTR_NAME)['get']
    assert description == ['app', 'test', 'read', 'getTest']
    assert http_method_name == 'get'
    assert view_class == TestInstanceView

    description, http_method_name, view_class = getattr(TestInstanceView, schema.REGISTRY_ATTR_NAME)['delete']
    assert description == ['app', 'test', 'write', 'deleteTest']
    assert http_method_name == 'delete'
    assert view_class == TestInstanceView


def test_feature_schema():
    feature_schema = schema.get_schema()

    assert feature_schema['listTests']['name'] == 'listTests'
    assert feature_schema['listTests']['coerced_url'] == '/api/1/test/'
    assert feature_schema['listTests']['description'] == ['app', 'test', 'read', 'listTests']
    assert feature_schema['listTests']['groups'] == ['app', 'test', 'read']

    assert feature_schema['getTest']['name'] == 'getTest'
    assert feature_schema['getTest']['coerced_url'] == '/api/1/test/{id}/'
    assert feature_schema['getTest']['description'] == ['app', 'test', 'read', 'getTest']
    assert feature_schema['getTest']['groups'] == ['app', 'test', 'read']

    assert feature_schema['deleteTest']['name'] == 'deleteTest'
    assert feature_schema['deleteTest']['coerced_url'] == '/api/1/test/{id}/'
    assert feature_schema['deleteTest']['description'] == ['app', 'test', 'write', 'deleteTest']
    assert feature_schema['deleteTest']['groups'] == ['app', 'test', 'write']


def test_feature_schema_configured_set_http_method_names():
    assert TestListView.http_method_names == ['get']
    assert TestInstanceView.http_method_names == ['get', 'delete']
