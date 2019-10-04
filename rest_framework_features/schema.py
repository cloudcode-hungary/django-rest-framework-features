import re

from django.core.exceptions import ImproperlyConfigured
from django.template.loader import render_to_string
from rest_framework.schemas import SchemaGenerator

from . import settings

REGISTRY_ATTR_NAME = '_feature_schema'
_schema_cache = None
_humanize_pattern = re.compile(r'([a-z]|[0-9]+[a-z]?|[A-Z]?)([A-Z0-9])')


def view(*groups, **features):
    def decorator(view_class):
        if not features:
            raise ImproperlyConfigured('TODO invalid decorator, no http method names')
        for http_method_name, feature_name in features.items():
            description = list(groups)
            if isinstance(feature_name, (list, tuple)):
                for f in feature_name:
                    description.append(f)
            else:
                description.append(feature_name)
            registry = getattr(view_class, REGISTRY_ATTR_NAME, {})
            registry[http_method_name] = (
                description,
                http_method_name,
                view_class,
            )
            setattr(view_class, REGISTRY_ATTR_NAME, registry)
        if settings.feature_settings.SET_HTTP_METHOD_NAMES:
            setattr(view_class, 'http_method_names', list(features.keys()))
        return view_class

    return decorator


def get_schema(use_cache=True):
    global _schema_cache
    if use_cache and _schema_cache:
        return _schema_cache
    generator = SchemaGenerator()
    enumerator = generator.endpoint_inspector_cls()
    end_points = enumerator.get_api_endpoints()
    schema = {}
    for url, http_method_name, view_func in end_points:
        generated_view = generator.create_view(view_func, http_method_name, None)
        coerced_url = generator.coerce_path(url, http_method_name, generated_view)
        try:
            feature = getattr(view_func.cls, REGISTRY_ATTR_NAME)[http_method_name.lower()]
        except AttributeError:
            raise ImproperlyConfigured('TODO missing view definition')
        description, http_method_name, view_class = feature
        *groups, feature_name = description
        if feature_name in schema:
            raise ImproperlyConfigured('TODO duplicate feature name')
        if re.match(r'\s', feature_name):
            raise ImproperlyConfigured('TODO not white space in feature name')
        verbose_name = _humanize_pattern.sub(r'\1 \2', feature_name).lower()
        feature_def = dict(
            name=feature_name,
            url=url,
            coerced_url=coerced_url,
            http_method_name=http_method_name,
            view_class=view_class,
            groups=groups,
            description=description,
            verbose_name=verbose_name,
        )
        schema[feature_name] = feature_def
    _schema_cache = schema
    return schema


def render_schema(*args, **kwargs):
    context = kwargs.pop('context', {})
    schema = get_schema()
    context.update(schema=schema)
    return render_to_string(
        *args, **kwargs, context=context
    )


def render_json_schema():
    return render_schema('rest_framework_features/feature_schema.json')


def render_locale_js_schema():
    return render_schema('rest_framework_features/feature_locale.js')


def render_locale_py_schema():
    return render_schema('rest_framework_features/feature_locale.py')


__all__ = (
    'REGISTRY_ATTR_NAME',
    'view',
    'get_schema',
    'render_schema',
    'render_json_schema',
    'render_locale_js_schema',
    'render_locale_py_schema',
)
