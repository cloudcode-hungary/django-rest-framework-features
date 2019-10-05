# Schema

## view

The most important entry point for rest-framework-features.

Example usage:
```python
from rest_framework import generics
from rest_framework_features import schema

@schema.view('test', get='getTest')
class TestRetrieveView(generics.RetrieveAPIView):
    ...
```

### `def view(*groups, **features):`   
This method will decorate the rest framework api views with extra information to generate the schema 
and manage permissions.

#### `*groups`
Used to define a tree of features. This is useful when used in combination with the permissions module. 
To read more about permissions click [here.](permissions.md)

#### `**features`
The keys must be a subset of the available http verbs 
(`get`, `post`, `put`, `patch`, `delete`, `head`, `options`, `trace`).
These names will be used for resolving features.
A value can also be a list or a tuple, to have it added to the permission groups.
In this case the last element will be the feature name, e.g.:

```python
from rest_framework import generics
from rest_framework_features import schema

@schema.view('test', get=('read', 'getTest'), delete=('write', 'deleteTest'))
class TestRetrieveView(generics.RetrieveDestroyAPIView):
    ...
```

- feature names must not contain white spaces.
- feature names must be unique all over the application.
- feature names should be lower camel case.

## get_schema

Method to resolve all information based on view decorations.

### `def get_schema(use_cache=True):`
This method uses `rest_framework.schemas.SchemaGenerator` to build a dictionary with keys of the feature names
and values as the definitions the these features. The values will be a dict of 
(`name`, `url`, `coerced_url`, `http_method_name`, `groups`, `description`, `verbose_name`, `view_class`).

#### `use_cache=True`
The generated schema is cached globally by default, as views are statically decorated. 
To force regeneration of the schema, call with `use_cache=False`

#### `returns`
```python
{
    'getTest': {
        'name': 'getTest',
        'url': '/api/1/test/{pk}/',
        'coerced_url': '/api/1/test/{id}/',
        'http_method_name': 'get',
        'groups': ['test'],
        'description': ['test', 'getTest'],
        'verbose_name': 'get test',
        'view_class': <class 'app.views.TestRetrieveView'>,
    },
}
```

## render_schema

Method to render the generated schema with a template.

### `def render_schema(*args, **kwargs):`   
This method will call `django.template.loader.render_to_string` with the provided arguments.
The context will include the `schema` variable, like the result of `get_schema()` method.

## render_json_schema

Method to generate the JSON schema of the api, which can be served, or provded to the frontend source code.

### `def render_json_schema():`

Calls render_schema with the provided `rest_framework_features/feature_schema.json` template.

#### `returns`
```json
{
  "listTests": {
    "url": "/api/1/test/",
    "method": "get"
  },
  "getTest": {
    "url": "/api/1/test/{id}/",
    "method": "get"
  },
  "deleteTest": {
    "url": "/api/1/test/{id}/delete/",
    "method": "delete"
  }
}
```

## render_locale_js_schema

Method to generate the JSON schema of the api, which can be served, or provded to the frontend source code.

### `def render_locale_js_schema():`

Calls render_schema with the provided `rest_framework_features/feature_locale.js` template.

#### `returns`
```javascript
(function () {
  return {
    listTests: window.django.pgettext('api', 'list tests'),
    getTest: window.django.pgettext('api', 'get test'),
    deleteTest: window.django.pgettext('api', 'delete test'),
  }
})
```

## render_locale_py_schema

Method to generate the JSON schema of the api, which can be served, or provded to the frontend source code.

### `def render_locale_py_schema():`

Calls render_schema with the provided `rest_framework_features/feature_locale.py` template.

#### `returns`
```python
from django.utils.translation import pgettext

API = {
    'listTests': pgettext('api', 'list tests'),
    'getTest': pgettext('api', 'get test'),
    'deleteTest': pgettext('api', 'delete test'),
}
```