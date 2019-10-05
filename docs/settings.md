# Settings

Settings for REST framework features are all namespaced in the REST_FRAMEWORK_FEATURES setting.
For example your project's `settings.py` file might look like this:

```python
REST_FRAMEWORK_FEATURES = {
    'ENABLE_PERMISSIONS': True,
}
```

The settings module provides the `feature_settings` object, that is used to access
REST framework features settings, checking for user settings first, then falling
back to the defaults.

## ENABLE_PERMISSIONS 
### `default: False`

When enabled, using `django.db.models.signals.post_migrate` all permissions
are synchronized with the current database. If a feature no longer exists,
the permissions will be removed. Based on the permission tree defined on
the views, permission strings will be concatenated by underscores, 
prefixed with the app name rest_framework_features e.g.
(`'rest_framework_features.test'`, `'rest_framework_features.test_getTest'`, `'rest_framework_features.test_listTests'`).
The content_type for all of these permissions will refer to the model defined by `DB_MODEL` setting.

## ENABLE_FEATURES 
### `default: False`

When enabled, using `django.db.models.signals.post_migrate` all features
are synchronized with the current database. The model for features must be a subclass
of `rest_framework_features.models.AbstractBaseFeature`, and be defined by the `DB_MODEL` setting.
The feature models are created in a recursive tree structure, with parent references, e.g.
(`(name='test', parent=None, hierarchical_name='test')`, `name='getTest', parent='test', hierarchical_name='test/getTest'`) 

## DB_MODEL 
### `default: 'rest_framework_features.models.Feature'` 

This feature model is defined below:

```python
from django.db import models
from django.utils.translation import ugettext_lazy as _

class AbstractBaseFeature(models.Model):
    class Meta:
        abstract = True
        unique_together = ('parent', 'name')
        ordering = ('hierarchical_name',)

    name = models.CharField(...)
    parent = models.ForeignKey(to='self', null=True, ...)
    hierarchical_name = models.CharField(...)
    ...


class Feature(AbstractBaseFeature):
    class Meta:
        verbose_name = _('feature')
        verbose_name_plural = _('features')
```

To use your own model, simply subclass `AbstractBaseFeature`, configure it in the settings
and extend the functionality as you wish. To find out why you would want to do this, 
read more about examples, ideas [here.](settings.md) TODO not settings.md but examples.md


## SET_HTTP_METHOD_NAMES
### `default: False`

When enabled, defining a `rest_framework_features.schema.view` decorator on an api view will also set
the `http_method_names` attribute on the view_class based on the feature keys provided.
To understand why is this useful, see the below example:

```python
from rest_framework import generics
from rest_framework_features import schema

@schema.view('test', put='updateTest')
class TestUpdateView(generics.UpdateAPIView):
    ...
``` 

The following declaration would run into an error when processing the schema, as
`rest_framework.generics.UpdateAPIView` uses both `['put', 'patch']` methods, but
only one of them is named and used by the schema. What you could do, is 
define `http_method_names` manually on the view, or enable this setting, so
it can be automatically done for you.