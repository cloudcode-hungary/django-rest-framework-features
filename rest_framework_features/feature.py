from django.core.exceptions import ImproperlyConfigured
from rest_framework.schemas import SchemaGenerator


class Feature:
    _registry = {}
    _schema = None

    def __init__(self, **kwargs):
        self.__dict__.update(**kwargs)

    @classmethod
    def view(cls, *groups, **features):
        def decorator(view_class):
            if not features:
                raise ImproperlyConfigured('TODO invalid')
            for http_method_name, feature_name in features.items():
                description = list(groups)
                if isinstance(feature_name, (list, tuple)):
                    for f in feature_name:
                        description.append(f)
                else:
                    description.append(feature_name)
                cls._registry[view_class] = (
                    description,
                    http_method_name,
                    view_class,
                )
            return view_class

        return decorator

    @classmethod
    def get_schema(cls):
        if cls._schema:
            return cls._schema
        generator = SchemaGenerator()
        enumerator = generator.endpoint_inspector_cls()
        end_points = enumerator.get_api_endpoints()
        schema = {}
        for url, http_method_name, view_func in end_points:
            view = generator.create_view(view_func, http_method_name, None)
            coerced_url = generator.coerce_path(url, http_method_name, view)
            try:
                feature = cls._registry[view_func.cls]
            except KeyError:
                raise ImproperlyConfigured('TODO missing view definition')
            description, http_method_name, view_class = feature
            *groups, feature_name = description
            if feature_name in schema:
                raise ImproperlyConfigured('TODO duplicate feature name')
            schema[feature_name] = cls(
                feature_name=feature_name,
                url=url,
                coerced_url=coerced_url,
                http_method_name=http_method_name,
                view_class=view_class,
                groups=groups,
                description=description,
            )
        cls._schema = schema
        return schema


__all__ = (
    'Feature',
)