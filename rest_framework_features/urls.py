from django.urls import NoReverseMatch

from .feature import Feature


def reverse(feature_name, **kwargs):
    schema = Feature.get_schema()
    try:
        feature = schema[feature_name]
    except KeyError:
        raise NoReverseMatch(feature_name)
    print(feature.url, feature.coerced_url, kwargs)
