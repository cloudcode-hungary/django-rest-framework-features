from django.core.exceptions import ImproperlyConfigured
from rest_framework.schemas import SchemaGenerator

REGISTRY_ATTR_NAME = '_feature_schema'
_schema_cache = None


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
        return view_class

    return decorator


def get_schema(cache=True):
    global _schema_cache
    if cache and _schema_cache:
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
        feature_def = dict(
            name=feature_name,
            url=url,
            coerced_url=coerced_url,
            http_method_name=http_method_name,
            view_class=view_class,
            groups=groups,
            description=description,
        )
        schema[feature_name] = feature_def
    _schema_cache = schema
    return schema


__all__ = (
    'REGISTRY_ATTR_NAME',
    'view',
    'get_schema',
)
