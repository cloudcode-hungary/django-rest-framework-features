import json
from unittest import mock

from django.core.management import call_command


def test_features_schema_json():
    stdout = mock.MagicMock()
    call_command('features', json=True, stdout=stdout)

    assert stdout.write.call_args == mock.call(json.dumps({
        'listTests': {'url': '/api/1/test/', 'method': 'get'},
        'getTest': {'url': '/api/1/test/{id}/', 'method': 'get'},
        'deleteTest': {'url': '/api/1/test/{id}/', 'method': 'delete'}
    }).replace(' ', '') + '\n')


def test_features_schema_locale_js():
    stdout = mock.MagicMock()
    call_command('features', locale_js=True, stdout=stdout)

    assert stdout.write.call_args == mock.call(
        '(function () {\n'
        '  return {\n'
        '''    listTests: window.django.pgettext('api', 'list tests'),\n'''
        '''    getTest: window.django.pgettext('api', 'get test'),\n'''
        '''    deleteTest: window.django.pgettext('api', 'delete test'),\n'''
        '  }\n'
        '})\n'
    )


def test_features_schema_locale_py():
    stdout = mock.MagicMock()
    call_command('features', locale_py=True, stdout=stdout)

    assert stdout.write.call_args == mock.call(
        'from django.utils.translation import pgettext\n\n'
        'API = {\n'
        '''    'listTests': pgettext('api', 'list tests'),\n'''
        '''    'getTest': pgettext('api', 'get test'),\n'''
        '''    'deleteTest': pgettext('api', 'delete test'),\n'''
        '}\n'
    )


def test_openapi_schema_generation_with_operation_id_overrides():
    stdout = mock.MagicMock()
    call_command('generateschema', stdout=stdout, format='openapi-json')

    result = stdout.write.call_args[0][0]

    assert '"operationId": "listTests"' in result
    assert '"operationId": "getTest"' in result
    assert '"operationId": "deleteTest"' in result
