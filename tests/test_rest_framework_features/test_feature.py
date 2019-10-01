from rest_framework_features import Feature
from tests.views import TestListView, TestRetrieveDestroyView


def test_feature_view_decorator():
    description, http_method_name, view_class = getattr(TestListView, Feature._registry_attr_name)['get']
    assert description == ['app', 'test', 'listTests']
    assert http_method_name == 'get'
    assert view_class == TestListView

    description, http_method_name, view_class = getattr(TestRetrieveDestroyView, Feature._registry_attr_name)['get']
    assert description == ['app', 'test', 'getTest']
    assert http_method_name == 'get'
    assert view_class == TestRetrieveDestroyView

    description, http_method_name, view_class = getattr(TestRetrieveDestroyView, Feature._registry_attr_name)['delete']
    assert description == ['app', 'test', 'deleteTest']
    assert http_method_name == 'delete'
    assert view_class == TestRetrieveDestroyView


def test_feature_schema():
    schema = Feature.get_schema()
    assert schema['listTests'].name == 'listTests'
    assert schema['listTests'].coerced_url == '/api/1/test/'
    assert schema['listTests'].description == ['app', 'test', 'listTests']
    assert schema['listTests'].groups == ['app', 'test']
