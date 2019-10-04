from django.urls import NoReverseMatch
from rest_framework.test import APIClient

from . import schema, urls


class FeatureAPIClient(APIClient):
    def __call__(self, feature_name, kwargs=None, **extra):
        feature_schema = schema.get_schema()
        try:
            feature_def = feature_schema[feature_name]
        except KeyError:
            raise NoReverseMatch(feature_name)
        else:
            path = urls.substitute(feature_def['coerced_url'], kwargs or {})
            method = feature_def['http_method_name']
            return getattr(self, method)(
                path=path,
                **extra,
            )


__all__ = (
    'FeatureAPIClient',
)
