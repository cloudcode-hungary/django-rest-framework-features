from django.core.exceptions import ImproperlyConfigured
from rest_framework.schemas import SchemaGenerator


class Feature:
    _registry_attr_name = '_feature'
    _schema = None

    def __init__(self, name, url, coerced_url, http_method_name, view_class, groups, description):
        self.name = name
        self.url = url
        self.coerced_url = coerced_url
        self.http_method_name = http_method_name
        self.view_class = view_class
        self.groups = groups
        self.description = description

    @classmethod
    def view(cls, *groups, **features):
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
                registry = getattr(view_class, cls._registry_attr_name, {})
                registry[http_method_name] = (
                    description,
                    http_method_name,
                    view_class,
                )
                setattr(view_class, cls._registry_attr_name, registry)
            return view_class

        return decorator

    @classmethod
    def get_schema(cls, cache=True):
        if cache and cls._schema:
            return cls._schema
        generator = SchemaGenerator()
        enumerator = generator.endpoint_inspector_cls()
        end_points = enumerator.get_api_endpoints()
        schema = {}
        for url, http_method_name, view_func in end_points:
            view = generator.create_view(view_func, http_method_name, None)
            coerced_url = generator.coerce_path(url, http_method_name, view)
            try:
                feature = getattr(view_func.cls, cls._registry_attr_name)[http_method_name.lower()]
            except AttributeError:
                raise ImproperlyConfigured('TODO missing view definition')
            description, http_method_name, view_class = feature
            *groups, feature_name = description
            if feature_name in schema:
                raise ImproperlyConfigured('TODO duplicate feature name')
            schema[feature_name] = cls(
                name=feature_name,
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
